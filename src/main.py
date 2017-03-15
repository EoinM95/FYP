"""Read a corpus, check there's a vector for everything"""
import os
import numpy as np
from vector_reader import read_vectors_from_file
from corpus_parser import read_parsed
from sentence_splitter import split, tokenize
from utilities import remove_stop_words, sum_of_vectors, DO_NOT_INCLUDE, stem, tag
from features import calculate_feature_vectors
#from neural_net import NeuralNetwork
from nb_classifier import NBClassifier

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
    training_set, test_set = train_and_test_split(processed_corpus)
    #neural_net = train(training_set)
    classifier = train(training_set)
    test(classifier, test_set)
    #neural_net.save('./trained_model.tf')

def train_and_test_split(processed_corpus):
    """Return balanced training set for negatives and positives, use rest as test data"""
    positive_inputs = []
    negative_inputs = []
    for corpus_entry in processed_corpus:
        feature_matrix = corpus_entry['feature_vectors']
        scores_vector = corpus_entry['scores_list']
        for i, feature_vector in enumerate(feature_matrix):
            score = scores_vector[i]
            if score[0] == 1:
                positive_inputs.append(feature_vector)
            else:
                negative_inputs.append(feature_vector)
    training_pos_size = int(len(positive_inputs)/2)
    training_inputs = []
    training_outputs = []
    test_inputs = []
    test_outputs = []
    for i, t_input in enumerate(positive_inputs):
        if i < training_pos_size:
            training_inputs.append(t_input)
            training_outputs.append([1])
        else:
            test_inputs.append(t_input)
            test_outputs.append([1])
    for i, t_input in enumerate(negative_inputs):
        if i < 2*training_pos_size:
            training_inputs.append(t_input)
            training_outputs.append([0])
        else:
            test_inputs.append(t_input)
            test_outputs.append([0])
    print('Training set contains ', training_pos_size, 'summary-worthy sentences, total size =',
          len(training_inputs))
    print('Test set contains ', len(test_inputs), 'sentences')
    training_inputs = np.array(training_inputs, dtype='float32')
    training_outputs = np.array(training_outputs, dtype='float32')
    test_inputs = np.array(test_inputs, dtype='float32')
    test_outputs = np.array(test_outputs, dtype='float32')
    return ((training_inputs, training_outputs), (test_inputs, test_outputs))

def train(training_set):
    """Create and train neural network"""
    input_matrix, output_vector = training_set
    #neural_net = NeuralNetwork(input_matrix, output_vector)
    classifier = NBClassifier(input_matrix, output_vector)
    #print('Starting NeuralNetwork training...', flush=True)
    #neural_net.train()
    classifier.train()
    #return neural_net
    return classifier

def test(neural_net, test_set):#pylint: disable = R0914
    """Test neural network"""
    input_matrix, expected_output = test_set
    correct = 0
    true_positives = 0
    false_positives = 0
    false_negatives = 0
    generated_output = neural_net.feed(input_matrix)
    for i, output in enumerate(generated_output):
        expected = expected_output[i][0]
        output = round(output)
        if expected == output:
            correct += 1
        if expected == 1 and output == 1:
            true_positives += 1
        elif expected == 0 and output == 1:
            false_positives += 1
        elif expected == 1 and output == 0:
            false_negatives += 1
    success_rate = (correct / len(expected_output)) * 100
    precision = (true_positives / (true_positives + false_positives)) * 100
    recall = (true_positives / (true_positives + false_negatives)) * 100
    print('Success rate = ', success_rate, '%')
    print('Precision = ', precision, '%')
    print('Recall = ', recall, '%')

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
                processed = featurize_from_training(corpus_file)
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

def featurize_from_training(corpus_file):
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
    pos = tag(tokens)
    length = len(tokens)
    tokens = remove_stop_words(tokens)
    vector = sentence_vector(tokens, VECTOR_DICTIONARY)
    if vector is DO_NOT_INCLUDE:
        return vector
    return {'sentence': sentence, 'tokens':tokens, 'sentence_vec': vector,
            'pos': pos, 'length': length}

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
