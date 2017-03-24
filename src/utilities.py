"""Handy stuff for displaying, reading etc."""
import re
import sys
import numpy as np
from nltk import pos_tag #pylint: disable = E0401
from nltk.corpus import stopwords #pylint: disable = E0401
from nltk.stem.wordnet import WordNetLemmatizer #pylint: disable = E0401

SENTENCE_PATTERN = r'(?<!..Mr|.Mrs|..Dr|Prof|.Neb|.Nev)\. (?=[A-Z])'
TOKEN_PATTERN = "(?<=[A-Za-z0-9]) "
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

def split(text):
    """Splits text into sentences, returns list"""
    return re.split(SENTENCE_PATTERN, text)

def tokenize(sentence):
    """Return list of tokens in sentence"""
    sentence = re.sub(r'(\.|[0-9]*)', '', sentence)
    sentence = re.sub(r'(\n|\r\n)', ' ', sentence)
    sentence = sentence.strip()
    sentence = re.sub(r'\s', ' ', sentence)
    sentence = re.sub(r'  ', ' ', sentence)
    tokens = re.split(TOKEN_PATTERN, sentence.lower())
    return list(filter(lambda t: t != '' and t != ' ', tokens))

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
