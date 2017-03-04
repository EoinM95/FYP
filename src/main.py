"""Read a corpus, check there's a vector for everything"""
import os
import numpy as np
from vector_reader import read_vectors_from_file
from corpus_parser import read_parsed
from sentence_splitter import split, tokenize
from utilities import remove_stop_words, sum_of_vectors, DO_NOT_INCLUDE, stem
from features import calculate_feature_vectors
from neural_net import NeuralNetwork

VECTOR_DICTIONARY = {}
MISSING_WORDS = []
MISSING_WORDS_FILE = 'missing_words.txt'
VECTOR_FILE = '..\\GoogleNews-vectors-negative300.bin' #'..\\vectors.txt'
CORPUS_DIRECTORY = '..\\duc01_tagged_meo_data\\'
ACCEPTABLE = 0.1



def initialise():
    """Read in vectors, read in all scored summaries and corresponding originals for title+keywords
    Then calculate feature vectors for every sentence in every text"""
    global VECTOR_DICTIONARY #pylint: disable = W0603
    VECTOR_DICTIONARY = read_vectors_from_file(VECTOR_FILE)
    processed_corpus = find_files_and_process()
    with open(MISSING_WORDS_FILE, 'w') as write_stream:
        for missing_word in MISSING_WORDS:
            write_stream.write(missing_word +'\n')
    corpus_size = len(processed_corpus)
    split_size = int(corpus_size/2)
    neural_net = train(processed_corpus[:split_size])
    test(neural_net, processed_corpus[split_size:])
    neural_net.save('./trained_model.tf')

def train(processed_corpus):
    """Create and train neural network"""
    input_matrix = []
    output_vector = []
    for corpus_entry in processed_corpus:
        feature_matrix = corpus_entry['feature_vectors']
        for feature_vector in feature_matrix:
            input_matrix.append(feature_vector)
        scores_vector = corpus_entry['scores_list']
        for score in scores_vector:
            output_vector.append(score)
    input_matrix = np.array(input_matrix, dtype='float32')
    output_vector = np.array(output_vector, dtype='float32')
    neural_net = NeuralNetwork(input_matrix, output_vector, './trained_model.tf')
    #print('Starting NeuralNetwork training...', flush=True)
    #neural_net.train()
    return neural_net

def test(neural_net, processed_corpus):
    """Test neural network"""
    input_matrix = []
    expected_output = []
    for corpus_entry in processed_corpus:
        feature_matrix = corpus_entry['feature_vectors']
        for feature_vector in feature_matrix:
            input_matrix.append(feature_vector)
        scores_vector = corpus_entry['scores_list']
        for score in scores_vector:
            expected_output.append(score)
    input_matrix = np.array(input_matrix)
    expected_output = np.array(expected_output)
    correct = 0
    generated_output = neural_net.feed(input_matrix)
    for i, output in enumerate(generated_output):
        difference = abs(output - expected_output[i])
        if difference <= ACCEPTABLE:
            correct += 1
    success_rate = (correct / len(expected_output)) * 100
    print('Success rate = ', success_rate, '%')

def find_files_and_process():
    """Find all files which are usable and parse them, return feature vectors and scores"""
    file_counter = 0
    features_and_scores = []
    for subdir, dirs, files in os.walk(CORPUS_DIRECTORY): #pylint: disable = W0612
        for file in files:
            corpus_file = subdir + os.sep + file
            if os.path.isfile(corpus_file):
                file_counter += 1
                print('Started processing file no ', file_counter, flush=True)
                processed = parse_and_featurize_from_scored(corpus_file)
                if processed is not DO_NOT_INCLUDE:
                    features_and_scores.append(processed)
                else:
                    print('Excluding file ', file, 'reseting file counter', flush=True)
                    file_counter = file_counter - 1
    print('Found and processed ', file_counter, ' usable texts and scored summaries', flush=True)
    return features_and_scores

# def parse_and_featurize_from_orig(filename):
#     """Parse file and create feature_vectors for each of its sentences"""
#     parsed_doc = parse_original_text(filename)
#     doc_body = parsed_doc['text']
#     sentence_list = create_sentence_list(doc_body)
#     title_vector = clean_and_vectorize(parsed_doc['title'])
#     has_keywords = parsed_doc['has_keywords']
#     if not has_keywords:
#         keywords_vector = []
#     else:
#         keywords_vector = clean_and_vectorize(parsed_doc['keywords'])
#     return calculate_feature_vectors(sentence_list, title_vector, keywords_vector)

def parse_and_featurize_from_scored(corpus_file):
    """Parse file and create feature_vectors for each of its sentences"""
    parsed_doc = read_parsed(corpus_file)
    title_vector = clean_and_vectorize(parsed_doc['title'])
    sentence_list = []
    scores_list = []
    for sentence in parsed_doc['sentences']:
        list_entry = tokenize_and_vectorize(sentence['sentence'])
        if list_entry != DO_NOT_INCLUDE:
            sentence_list.append(list_entry)
            scores_list.append([sentence['in_summary']])
    feature_vectors = calculate_feature_vectors(sentence_list, title_vector)
    return {'feature_vectors': feature_vectors, 'scores_list': np.array(scores_list)}

def tokenize_and_vectorize(sentence):
    """Return tokens and vector for sentence"""
    tokens = tokenize(sentence)
    tokens = remove_stop_words(tokens)
    vector = sentence_vector(tokens, VECTOR_DICTIONARY)
    if vector is DO_NOT_INCLUDE:
        return vector
    return {'sentence': sentence, 'tokens':tokens, 'sentence_vec': vector}

def clean_and_vectorize(sentence):
    """Remove stop words and find vector"""
    vector = tokenize_and_vectorize(sentence)
    if vector is DO_NOT_INCLUDE:
        return vector
    return vector['sentence_vec']

def create_sentence_list(doc_body):
    """Return sentence data structure containing their vectors"""
    sentence_list = []
    sentences = split(doc_body)
    for sentence in sentences:
        list_entry = tokenize_and_vectorize(sentence)
        if list_entry is not DO_NOT_INCLUDE:
            sentence_list.append(list_entry)
    return sentence_list

def sentence_vector(sentence, vector_dictionary):
    """Will return vector which represents sentence"""
    word_vec_list = []
    for word in sentence:
        word = word.strip()
        stemmed = stem(word)
        if stemmed in vector_dictionary:
            word_vec = vector_dictionary[stemmed]
            word_vec_list.append(word_vec)
        elif word in vector_dictionary:
            word_vec = vector_dictionary[word]
            word_vec_list.append(word_vec)
        elif word not in MISSING_WORDS:
            MISSING_WORDS.append(word)
    if not word_vec_list:
        return DO_NOT_INCLUDE
    return sum_of_vectors(word_vec_list)

if __name__ == '__main__':
    initialise()
