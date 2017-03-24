"""Functions for building classifier and summariser"""
import os
import numpy as np
from corpus_parser import read_from_training, parse_from_new
from utilities import (remove_stop_words, sum_of_vectors, DO_NOT_INCLUDE,
                       stem, tag, show_progress, split, tokenize)
from features import calculate_feature_vectors
from classifier import build_and_test_classifier, restore_and_test_classifier

MISSING_WORDS = []
MISSING_WORDS_FILE = '../missing_words.txt'
CORPUS_DIRECTORY = '../duc01_tagged_meo_data/'
TEST_DOCS_DIRECTORY = '../test_docs/'
SAMPLE_SUMMARIES_DIRECTORY = '../sample_summaries/'
DUC_CORPUS_SIZE = 104
SAMPLE_DOCS_SIZE = 305
SENTENCE_FEATURES = 7

class Summariser():
    """Summariser class, use to summarise texts, needs to be passed pre-trained classifier"""
    def __init__(self, classifier, vector_dictionary):
        self.vector_dictionary = vector_dictionary
        self.classifier = classifier

    def summarise(self, text_file, output_file):
        """Extract feature_vectors, run through classifier and write summary to output_file"""
        processed = featurize_from_new(text_file, self.vector_dictionary)
        if processed is DO_NOT_INCLUDE:
            return False
        else:
            feature_vectors, sentence_list, title = processed
            labels = self.classifier.classify(feature_vectors)
            with open(output_file, 'w+') as output_stream:
                output_stream.write('Title: ' + title + '\n')
                for i, label in enumerate(labels):
                    if round(label) == 1:
                        output_stream.write(sentence_list[i]['sentence'] + '\n')
            return True

    def print_summary(self, text_file):
        """Extract feature_vectors, run through classifier and write summary to output_file"""
        feature_vectors, sentence_list, title = featurize_from_new(text_file,
                                                                   self.vector_dictionary)
        labels = self.classifier.classify(feature_vectors)
        print('Title: ' + title)
        for i, label in enumerate(labels):
            if round(label) == 1:
                print(sentence_list[i])

def build_summariser(vector_dictionary, classifier_type, trained_model_file=None):
    """Process the default corpus, train and test a classifier and return a summariser object"""
    if trained_model_file is None:
        processed_corpus = find_training_files_and_process(vector_dictionary)
        classifier = build_and_test_classifier(classifier_type, SENTENCE_FEATURES,
                                               processed_corpus)
    else:
        classifier = restore_and_test_classifier(classifier_type, SENTENCE_FEATURES,
                                                 trained_model_file)
    summariser = Summariser(classifier, vector_dictionary)
    return summariser


def find_training_files_and_process(vector_dictionary):
    """Find all files which are usable and parse them, return feature vectors and scores"""
    file_counter = 0
    features_and_scores = []
    print('Loading DUC training corpus...', flush=True)
    for subdir, dirs, files in os.walk(CORPUS_DIRECTORY): #pylint: disable = W0612
        for file in files:
            corpus_file = subdir + os.sep + file
            if os.path.isfile(corpus_file):
                file_counter += 1
                show_progress((file_counter/DUC_CORPUS_SIZE)*100)
                processed = featurize_from_training(corpus_file, vector_dictionary)
                if processed is not DO_NOT_INCLUDE:
                    features_and_scores.append(processed)
                else:
                    print('Excluding file ', file, 'reseting file counter', flush=True)
                    file_counter = file_counter - 1
    print('\nFound and processed ', file_counter, ' corpus texts with summaries', flush=True)
    with open(MISSING_WORDS_FILE, 'w') as write_stream:
        for missing_word in MISSING_WORDS:
            write_stream.write(missing_word +'\n')
    return features_and_scores

def find_sample_files_and_summarise(summariser):
    """Find all files which are usable and parse them, return feature vectors and scores"""
    file_counter = 0
    features_and_scores = []
    print('Summarising DUC sample texts...', flush=True)
    for subdir, dirs, files in os.walk(TEST_DOCS_DIRECTORY): #pylint: disable = W0612
        for file in files:
            sample_file = subdir + os.sep + file
            if os.path.isfile(sample_file):
                file_counter += 1
                show_progress((file_counter/SAMPLE_DOCS_SIZE)*100)
                summariser.summarise(sample_file,
                                     SAMPLE_SUMMARIES_DIRECTORY + file + '.summary')
    print('Found and summarised ', file_counter, ' texts', flush=True)
    with open(MISSING_WORDS_FILE, 'w') as write_stream:
        for missing_word in MISSING_WORDS:
            write_stream.write(missing_word +'\n')
    return features_and_scores


def featurize_from_new(filename, vector_dictionary):
    """Parse file and create feature_vectors for each of its sentences"""
    parsed_doc = parse_from_new(filename)
    if parsed_doc is DO_NOT_INCLUDE:
        return DO_NOT_INCLUDE
    doc_body = parsed_doc['doc_body']
    sentence_list = create_sentence_list(doc_body, vector_dictionary)
    title = parsed_doc['title']
    title_vector = clean_and_vectorize(title, vector_dictionary)
    return calculate_feature_vectors(sentence_list, title_vector), sentence_list, title

def featurize_from_training(corpus_file, vector_dictionary):
    """Parse file and create feature_vectors for each of its sentences"""
    parsed_doc = read_from_training(corpus_file)
    title_vector = clean_and_vectorize(parsed_doc['title'], vector_dictionary)
    sentence_list = []
    scores_list = []
    for sentence in parsed_doc['sentences']:
        list_entry = tokenize_and_vectorize(sentence['sentence'], vector_dictionary)
        if list_entry != DO_NOT_INCLUDE:
            sentence_list.append(list_entry)
            scores_list.append([sentence['in_summary']])
    feature_vectors = calculate_feature_vectors(sentence_list, title_vector)
    return {'feature_vectors': feature_vectors, 'scores_list': np.array(scores_list)}

def tokenize_and_vectorize(sentence, vector_dictionary):
    """Return tokens and vector for sentence"""
    tokens = tokenize(sentence)
    pos = tag(tokens)
    length = len(tokens)
    tokens = remove_stop_words(tokens)
    vector = sentence_vector(tokens, vector_dictionary)
    if vector is DO_NOT_INCLUDE:
        return vector
    return {'sentence': sentence, 'tokens':tokens, 'sentence_vec': vector,
            'pos': pos, 'length': length}

def clean_and_vectorize(sentence, vector_dictionary):
    """Remove stop words and find vector"""
    vector = tokenize_and_vectorize(sentence, vector_dictionary)
    if vector is DO_NOT_INCLUDE:
        return vector
    return vector['sentence_vec']

def create_sentence_list(doc_body, vector_dictionary):
    """Return sentence data structure containing their vectors"""
    sentence_list = []
    sentences = split(doc_body)
    for sentence in sentences:
        list_entry = tokenize_and_vectorize(sentence, vector_dictionary)
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
