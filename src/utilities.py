"""Handy stuff for displaying, reading etc."""
import sys
import numpy as np
from nltk import pos_tag #pylint: disable = E0401
from nltk.corpus import stopwords #pylint: disable = E0401
from nltk.stem.wordnet import WordNetLemmatizer #pylint: disable = E0401

DO_NOT_INCLUDE = -1

def stem(word):
    """Stem word using the PorterStemmer algorithm"""
    stemmer = WordNetLemmatizer()
    return stemmer.lemmatize(word)

def tag(sentence):
    """Return parts of speech for a sentence"""
    return pos_tag(sentence)

def show_progress(percent_progress):
    """Show a progress bar in the terminal"""
    sys.stdout.write('\r')
    sys.stdout.write("[%-20s] %d%%" % ('='*int(percent_progress/5), percent_progress))
    sys.stdout.flush()
    if percent_progress == 100:
        sys.stdout.write('\n')

def sum_of_vectors(vector_list):
    """Add a list of vectors, return vector representing the sum"""
    sum_vector = vector_list[0]
    for i in range(1, len(vector_list)-1):
        sum_vector = np.add(sum_vector, vector_list[i])
    return sum_vector


def remove_stop_words(word_list):
    """Remove useless words from list
        Stop words taken from http://www.ranks.nl/stopwords
    """
    stop_word_list = stopwords.words('english')
    return [word for word in word_list if word not in stop_word_list]
