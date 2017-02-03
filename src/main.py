"""Read a corpus, check there's a vector for everything"""
from vector_reader import read_vectors_from_file
from corpus_parser import parse_original_text
from sentence_splitter import split, tokenize
from utilities import remove_stop_words, sum_of_vectors
from features import calculate_feature_vectors
VECTOR_DICTIONARY = {}

def main():
    """Read data"""
    #need to maintain sentence position somehow
    #vector_file = input('Enter the location of the vector file\n')
    #vector_file = '..\\GoogleNews-vectors-negative300.bin'
    #global VECTOR_DICTIONARY #pylint: disable = W0603
    #VECTOR_DICTIONARY = read_vectors_from_file(vector_file)
    #text_file = input('Enter the filename of the text you wish to summarize\n')
    text_file = '..\\formal\\training\\formal-training\\categorization\\US-Foreign-Policy\\299\\docs\\WSJ911213-0036'
    parsed_doc = parse_original_text(text_file)
    doc_body = parsed_doc['text']
    sentence_list = create_sentence_list(doc_body)
    title_vector = clean_and_vectorize(parsed_doc['title'])
    keywords_vector = clean_and_vectorize(parsed_doc['keywords'])
    feature_vectors = calculate_feature_vectors(sentence_list, title_vector, keywords_vector)
    print(feature_vectors, '\n*******************************************************\n')

def clean_and_vectorize(sentence):
    """Remove stop words and find vector"""
    tokens = tokenize(sentence)
    tokens = remove_stop_words(tokens)
    return []#sentence_vector(tokens)

def create_sentence_list(doc_body):
    """Return sentence data structure containing their vectors"""
    sentence_list = []
    sentences = split(doc_body)
    for sentence in sentences:
        tokens = tokenize(sentence)
        tokens = remove_stop_words(tokens)
        sentence_vec = []#sentence_vector(tokens)
        dictionary_entry = {'sentence': sentence, 'sentence_vec': sentence_vec, 'tokens': tokens}
        sentence_list.append(dictionary_entry)
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
    return sum_of_vectors(word_vec_list)
main()
