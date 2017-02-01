"""Read a corpus, check there's a vector for everything"""
from vector_reader import read_vectors_from_file
from vector import sum_of_vectors
from corpus_parser import parse_original_text
from sentence_splitter import split, tokenize
from utilities import remove_stop_words
from features import calculate_feature_vectors
VECTOR_DICTIONARY = {}

def main():
    """Read data"""
    #need to maintain sentence position somehow
    vector_file = input('Enter the location of the vector file\n')
    global VECTOR_DICTIONARY #pylint: disable = W0603
    VECTOR_DICTIONARY = read_vectors_from_file(vector_file)
    text_file = input('Enter the filename of the text you wish to summarize\n')
    parsed_doc = parse_original_text(text_file)
    doc_body = parsed_doc['text']
    sentence_dict = sentence_dictionary(doc_body)
    title_vector = clean_and_vectorize(parsed_doc['title'])
    keywords_vector = clean_and_vectorize(parsed_doc['keywords'])
    feature_vectors = calculate_feature_vectors(sentence_dict, title_vector, keywords_vector)
    print(feature_vectors[0])

def clean_and_vectorize(sentence):
    """Remove stop words and find vector"""
    tokens = tokenize(sentence)
    tokens = remove_stop_words(tokens)
    return sentence_vector(tokens)

def sentence_dictionary(doc_body):
    """Return sentence data structure containing their vectors"""
    sentence_dict = {}
    sentence_list = split(doc_body)
    for sentence in sentence_list:
        tokens = tokenize(sentence)
        tokens = remove_stop_words(tokens)
        sentence_vec = sentence_vector(tokens)
        dictionary_entry = {'sentence_vec': sentence_vec, 'tokens': tokens}
        sentence_dict[sentence] = dictionary_entry
    return sentence_dict

def sentence_vector(sentence):
    """Will return vector which represents sentence"""
    word_vec_list = []
    for word in sentence:
        word_vec = VECTOR_DICTIONARY[word]
        word_vec_list.append(word_vec)
    return sum_of_vectors(word_vec_list)
