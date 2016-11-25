"""Read a corpus, check there's a vector for everything"""
from sentence_splitter import read_sentences_from_file
#from sentence import Sentence
from vector_reader import read_vectors_from_file
#from vector import Vector

def main():
    """Read data"""
    vector_file = input('Enter the location of the vector file')
    vector_dictionary = read_vectors_from_file(vector_file)
    text_file = input('Enter the filename of the text you wish to summarize')
    sentence_list = read_sentences_from_file(text_file)

def ts_isf(sentence):
    """Compute the mean """
    print('TO DO')
#need sentence position

def similairty_to_title(sentence, title):
    """Return simliarity of sentence to the title"""
    return sentence.vector().cosine_similarity(title.vector())

def similairty_to_keywords(sentence, keywords):
    """Return similarity of sentence to keywords of text"""
    print('TO DO')

def compute_centroid(sentences):
    """Return similarity of sentence to keywords of text"""
    print('TO DO')

def senetence_2_sentence_cohesion(sentences):
    """Return similarity of sentence to keywords of text"""
    print('TO DO')
