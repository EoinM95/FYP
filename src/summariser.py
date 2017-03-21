"""Functions for building classifier and summariser"""
import os
import re
import numpy as np
from corpus_parser import (read_from_duc, parse_from_new,
                           read_from_tipster_scored, read_title_from_tipster_orig)
from sentence_splitter import split, tokenize
from utilities import remove_stop_words, sum_of_vectors, DO_NOT_INCLUDE, stem, tag
from features import calculate_feature_vectors
from classifier import build_and_test_classifier

MISSING_WORDS = []
MISSING_WORDS_FILE = 'missing_words.txt'
TEST_CORPUS_DIRECTORY = '..\\duc01_tagged_meo_data\\'
TIPSTER_SCORED_DIRECTORY = '..\\composite_summaries\\tipster-composite-summaries\\'
TS_DIRECT_PATTERN = r'\\composite_summaries\\tipster-composite-summaries\\'
TIPSTER_ORIG_DIRECT_PATTERN = r'\\formal\\test\\formal-test\\'
TIPSTER_FILE_PATTERN = r'(?P<file_name>WSJ[0-9]+-[0-9]+)(?P<extension>\.sents\.scored)'
SENTENCE_FEATURES = 7

class Summariser():
    """Summariser class, use to summarise texts, needs to be passed pre-trained classifier"""
    def __init__(self, classifier, vector_dictionary):
        self.vector_dictionary = vector_dictionary
        self.classifier = classifier

    def summarise(self, text_file, output_file):
        """Extract feature_vectors, run through classifier and write summary to output_file"""
        feature_vectors, sentence_list = featurize_from_new(text_file, self.vector_dictionary)
        labels = self.classifier.predict(feature_vectors)
        with open(output_file, 'w+') as output_stream:
            for i, label in enumerate(labels):
                if round(label) == 1:
                    output_stream.write(sentence_list[i])

    def print_summary(self, text_file):
        """Extract feature_vectors, run through classifier and write summary to output_file"""
        feature_vectors, sentence_list = featurize_from_new(text_file, self.vector_dictionary)
        labels = self.classifier.predict(feature_vectors)
        for i, label in enumerate(labels):
            if round(label) == 1:
                print(sentence_list[i])

def build_summariser(vector_dictionary, classifier_type, trained_model_file=None):
    """Process the default corpus, train and test a classifier and return a summariser object"""
    training_corpus = find_training_files_and_process(vector_dictionary)
    test_corpus = find_test_files_and_process(vector_dictionary)
    classifier = build_and_test_classifier(classifier_type, SENTENCE_FEATURES,
                                           training_corpus, test_corpus, trained_model_file)
    summariser = Summariser(classifier, vector_dictionary)
    return summariser


def find_test_files_and_process(vector_dictionary):
    """Find all files which are usable and parse them, return feature vectors and scores"""
    file_counter = 0
    features_and_scores = []
    for subdir, dirs, files in os.walk(TEST_CORPUS_DIRECTORY): #pylint: disable = W0612
        for file in files:
            corpus_file = subdir + os.sep + file
            if os.path.isfile(corpus_file):
                file_counter += 1
                print('Started processing file no ', file_counter, flush=True)
                processed = featurize_from_duc(corpus_file, vector_dictionary)
                if processed is not DO_NOT_INCLUDE:
                    features_and_scores.append(processed)
                else:
                    print('Excluding file ', file, 'reseting file counter', flush=True)
                    file_counter = file_counter - 1
    print('Found and processed ', file_counter, ' usable texts and scored summaries', flush=True)
    with open(MISSING_WORDS_FILE, 'w') as write_stream:
        for missing_word in MISSING_WORDS:
            write_stream.write(missing_word +'\n')
    return features_and_scores

def find_training_files_and_process(vector_dictionary):
    """Find all files which are usable and parse them, return feature vectors and scores"""
    file_counter = 0
    file_regex = re.compile(TIPSTER_FILE_PATTERN)
    directory_regex = re.compile(TS_DIRECT_PATTERN)
    features_and_scores = []
    for subdir, dirs, files in os.walk(TIPSTER_SCORED_DIRECTORY): #pylint: disable = W0612
        for file in files:
            match = file_regex.match(file)
            if match:
                scored_filepath = subdir + os.sep + file
                original_file = match.group('file_name')
                original_directory = directory_regex.sub(TIPSTER_ORIG_DIRECT_PATTERN, subdir)
                original_filepath = original_directory+os.sep+original_file
                if os.path.isfile(original_filepath):
                    file_counter += 1
                    print('Started processing file no ', file_counter, flush=True)
                    tag_type = 'categ'
                    if 'adhoc' in scored_filepath:
                        tag_type = 'adhoc'
                    processed = featurize_from_tipster(scored_filepath,
                                                       original_filepath,
                                                       vector_dictionary, tag_type)
                    if processed is not DO_NOT_INCLUDE:
                        features_and_scores.append(processed)
                    else:
                        print('Excluding file ', file, 'reseting file counter', flush=True)
                        file_counter = file_counter - 1
                else:
                    print('Couldn\'t find matching original for scored summary: ', scored_filepath)
    print('Found and processed ', file_counter, ' usable texts and scored summaries', flush=True)
    return features_and_scores


def featurize_from_new(filename, vector_dictionary):
    """Parse file and create feature_vectors for each of its sentences"""
    parsed_doc = parse_from_new(filename)
    doc_body = parsed_doc['text']
    sentence_list = create_sentence_list(doc_body, vector_dictionary)
    title_vector = clean_and_vectorize(parsed_doc['title'], vector_dictionary)
    return calculate_feature_vectors(sentence_list, title_vector)

def featurize_from_duc(corpus_file, vector_dictionary):
    """Parse file and create feature_vectors for each of its sentences"""
    parsed_doc = read_from_duc(corpus_file)
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

def featurize_from_tipster(scored_file, original_file, vector_dictionary, tag_type='categ'):
    """Parse file and create feature_vectors for each of its sentences"""
    title_vector = clean_and_vectorize(read_title_from_tipster_orig(original_file),
                                       vector_dictionary)
    scored_sentences = read_from_tipster_scored(scored_file, tag_type)
    if scored_sentences is DO_NOT_INCLUDE:
        return DO_NOT_INCLUDE
    sentence_list = []
    scores_list = []
    for sentence in scored_sentences:
        list_entry = tokenize_and_vectorize(sentence['sentence'], vector_dictionary)
        if list_entry != DO_NOT_INCLUDE:
            sentence_list.append(list_entry)
            scores_list.append([sentence['best_score']])
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
