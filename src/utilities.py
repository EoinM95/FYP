"""Handy stuff for displaying, reading etc."""
import sys
import numpy as np
from nltk.stem.wordnet import WordNetLemmatizer #pylint: disable = E0401

DO_NOT_INCLUDE = -1

def stem(word):
    """Stem word using the PorterStemmer algorithm"""
    stemmer = WordNetLemmatizer()
    return stemmer.lemmatize(word)

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
    stop_word_list = ['a', 'about', 'above', 'after', 'again', 'against', 'all',
                      'am', 'an', 'and', 'any', 'are', 'aren\'t', 'as', 'at', 'be',
                      'because',
                      'been',
                      'before',
                      'being',
                      'below',
                      'between',
                      'both',
                      'but',
                      'by',
                      'can\'t',
                      'cannot',
                      'could',
                      'couldn\'t',
                      'did',
                      'didn\'t',
                      'do',
                      'does',
                      'doesn\'t',
                      'doing',
                      'don\'t',
                      'down',
                      'during',
                      'each',
                      'few',
                      'for',
                      'from',
                      'further',
                      'had',
                      'hadn\'t',
                      'has',
                      'hasn\'t',
                      'have',
                      'haven\'t',
                      'having',
                      'he',
                      'he\'d',
                      'he\'ll',
                      'he\'s',
                      'her',
                      'here',
                      'here\'s',
                      'hers',
                      'herself',
                      'him',
                      'himself',
                      'his',
                      'how',
                      'how\'s',
                      'i',
                      'i\'d',
                      'i\'ll',
                      'i\'m',
                      'i\'ve',
                      'if',
                      'in',
                      'into',
                      'is',
                      'isn\'t',
                      'it',
                      'it\'s',
                      'its',
                      'itself',
                      'let\'s',
                      'me',
                      'more',
                      'most',
                      'mustn\'t',
                      'my',
                      'myself',
                      'no',
                      'nor',
                      'not',
                      'of',
                      'off',
                      'on',
                      'once',
                      'only',
                      'or',
                      'other',
                      'ought',
                      'our',
                      'ours',
                      'ourselves',
                      'out',
                      'over',
                      'own',
                      'same',
                      'shan\'t',
                      'she',
                      'she\'d',
                      'she\'ll',
                      'she\'s',
                      'should',
                      'shouldn\'t',
                      'so',
                      'some',
                      'such',
                      'than',
                      'that',
                      'that\'s',
                      'the',
                      'their',
                      'theirs',
                      'them',
                      'themselves',
                      'then',
                      'there',
                      'there\'s',
                      'these',
                      'they',
                      'they\'d',
                      'they\'ll',
                      'they\'re',
                      'they\'ve',
                      'this',
                      'those',
                      'through',
                      'to',
                      'too',
                      'under',
                      'until',
                      'up',
                      'very',
                      'was',
                      'wasn\'t',
                      'we',
                      'we\'d',
                      'we\'ll',
                      'we\'re',
                      'we\'ve',
                      'were',
                      'weren\'t',
                      'what',
                      'what\'s',
                      'when',
                      'when\'s',
                      'where',
                      'where\'s',
                      'which',
                      'while',
                      'who',
                      'who\'s',
                      'whom',
                      'why',
                      'why\'s',
                      'with',
                      'won\'t',
                      'would',
                      'wouldn\'t',
                      'you',
                      'you\'d',
                      'you\'ll',
                      'you\'re',
                      'you\'ve',
                      'your',
                      'yours',
                      'yourself',
                      'yourselves']

    return [word for word in word_list if word not in stop_word_list]
