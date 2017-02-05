"""Read a corpus, check there's a vector for everything"""
import re
import os
from vector_reader import read_vectors_from_file
from corpus_parser import parse_original_text, parse_scored_text
from sentence_splitter import split, tokenize
from utilities import remove_stop_words, sum_of_vectors, DO_NOT_INCLUDE
from features import calculate_feature_vectors

VECTOR_DICTIONARY = {}
VECTOR_FILE = '..\\GoogleNews-vectors-negative300.bin'
SCORED_TEST_DIRECTORY = '..\\composite_summaries\\tipster-composite-summaries\\'
ST_DIRECT_PATTERN = r'\\composite_summaries\\tipster-composite-summaries\\'
ORIGINALS_DIRECT_PATTERN = r'\\formal\\test\\formal-test\\'
FILE_NAME_PATTERN = r'(?P<file_name>WSJ[0-9]+-[0-9]+)(?P<extension>\.sents\.scored)'


def train():
    """Read in vectors, read in all scored summaries and corresponding originals for title+keywords
    Then calculate feature vectors for every sentence in every text"""
    global VECTOR_DICTIONARY #pylint: disable = W0603
    VECTOR_DICTIONARY = read_vectors_from_file(VECTOR_FILE)
    file_counter = 0
    file_regex = re.compile(FILE_NAME_PATTERN)
    directory_regex = re.compile(ST_DIRECT_PATTERN)
    for subdir, dirs, files in os.walk(SCORED_TEST_DIRECTORY): #pylint: disable = W0612
        for file in files:
            match = file_regex.match(file)
            if match:
                scored_filepath = subdir + os.sep + file
                original_file = match.group('file_name')
                original_directory = directory_regex.sub(ORIGINALS_DIRECT_PATTERN, subdir)
                original_filepath = original_directory+os.sep+original_file
                if os.path.isfile(original_filepath):
                    file_counter = file_counter + 1
                    print('Started processing file no ', file_counter) # can do these in parallel processes
                    if file_counter == 145:
                        print(scored_filepath)
                    tag_type = 'categ'
                    if 'adhoc' in scored_filepath:
                        tag_type = 'adhoc'
                    processed = parse_and_featurize_from_scored(scored_filepath,
                                                                original_filepath, tag_type)
                    if processed is not DO_NOT_INCLUDE:
                        feature_vectors = processed['feature_vectors']
                        scores_list = processed['scores_list']
                        print(feature_vectors[0])
                        print(scores_list[0])
                    else:
                        print('Excluding file ', file, 'reseting file counter')
                        file_counter = file_counter - 1
                else:
                    print('Couldn\'t find matching original for scored summary with filename: ', scored_filepath)
    print(file_counter)

def parse_and_featurize_from_orig(filename):
    """Parse file and create feature_vectors for each of its sentences"""
    parsed_doc = parse_original_text(filename)
    doc_body = parsed_doc['text']
    sentence_list = create_sentence_list(doc_body)
    title_vector = clean_and_vectorize(parsed_doc['title'])
    has_keywords = parsed_doc['has_keywords']
    if not has_keywords:
        keywords_vector = []
    else:
        keywords_vector = clean_and_vectorize(parsed_doc['keywords'])
    return calculate_feature_vectors(sentence_list, title_vector, keywords_vector, has_keywords)

def parse_and_featurize_from_scored(scored_file, original_file, tag_type='categ'):
    """Parse file and create feature_vectors for each of its sentences"""
    scored_sentences = parse_scored_text(scored_file, tag_type)
    if scored_sentences is DO_NOT_INCLUDE:
        return DO_NOT_INCLUDE
    sentence_list = []
    scores_list = []
    for sentence in scored_sentences:
        list_entry = tokenize_and_vectorize(sentence['sentence'])
        if list_entry != DO_NOT_INCLUDE:
            sentence_list.append(list_entry)
            scores_list.append(sentence['best_score'])
    original_parsed = parse_original_text(original_file)
    title_vector = clean_and_vectorize(original_parsed['title'])
    has_keywords = original_parsed['has_keywords']
    if not has_keywords:
        keywords_vector = []
    else:
        keywords_vector = clean_and_vectorize(original_parsed['keywords'])
        if keywords_vector is DO_NOT_INCLUDE:
            has_keywords = False
    feature_vectors = calculate_feature_vectors(sentence_list, title_vector, keywords_vector, has_keywords)
    return {'feature_vectors': feature_vectors, 'scores_list': scores_list}

def tokenize_and_vectorize(sentence):
    """Return tokens and vector for sentence"""
    tokens = tokenize(sentence)
    tokens = remove_stop_words(tokens)
    vector = sentence_vector(tokens)
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
        tokens = tokenize(sentence)
        tokens = remove_stop_words(tokens)
        sentence_vec = sentence_vector(tokens)
        list_entry = {'sentence': sentence, 'sentence_vec': sentence_vec, 'tokens': tokens}
        sentence_list.append(list_entry)
    return sentence_list

def sentence_vector(sentence):
    """Will return vector which represents sentence"""
    word_vec_list = []
    for word in sentence:
        word = word.strip()
        if word in VECTOR_DICTIONARY:
            word_vec = VECTOR_DICTIONARY[word]
            word_vec_list.append(word_vec)
        else:
            print('Error, couldn\'t find word: ', word)
    if not word_vec_list:
        return DO_NOT_INCLUDE
    return sum_of_vectors(word_vec_list)
train()
