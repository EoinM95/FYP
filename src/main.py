"""Read a corpus, check there's a vector for everything"""
from sentence_splitter import read_sentences_from_file
from sentence import Sentence
from vector_reader import read_vectors_from_file
from vector import Vector

def main():
    """Read data"""
    vector_file = input('Enter the location of the vector file')
    vector_dictionary = read_vectors_from_file(vector_file)
    text_file = input('Enter the filename of the text you wish to summarize')
    sentence_list = read_sentences_from_file(text_file)
