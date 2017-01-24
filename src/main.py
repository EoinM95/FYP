"""Read a corpus, check there's a vector for everything"""
from math import log2
from collections import Counter
from sentence_splitter import read_sentences_from_file
from vector_reader import read_vectors_from_file
from vector import sum_of_vectors
import numpy as np
VECTOR_DICTIONARY = {}
def main():
    """Read data"""
    #need to maintain sentence position somehow
    vector_file = input('Enter the location of the vector file')
    global VECTOR_DICTIONARY
    VECTOR_DICTIONARY = read_vectors_from_file(vector_file)
    text_file = input('Enter the filename of the text you wish to summarize')
    sentence_list = read_sentences_from_file(text_file)
    sentence_vectors = list(map(sentence_vector, sentence_list))


def compute_tf_isfs_for_text(sentences):
    """Compute the mean term frequency*inverse sentence frequency for
    all words of sentence, for every sentence. Analagous to tf*idf"""
    sentence_results = {}
    num_of_sentences = len(sentences)
    sentence_word_counts = {}
    word_appearances = {}
    for sentence in sentences:
        word_counter = Counter(sentence)
        sentence_word_counts[sentence] = word_counter
        for word in word_counter.keys():
            word_appearances[word] = word_appearances.get(word, default=0) + 1
    for sentence in sentences:
        word_tfisfs = []
        for word in sentence:
            tf = sentence_word_counts[sentence][word]
            num_of_s_containing_word = word_appearances[word]
            isf = log2(num_of_sentences/num_of_s_containing_word)
            word_tfisfs.append(tf*isf)
        sentence_results[sentence] = np.mean(np.array(word_tfisfs))
    return sentence_results


def similairty_to_title(sentence_vec, title_vector):
    """Return simliarity of sentence to the title"""
    return sentence_vec.similarity(title_vector)

def similairty_to_keywords(sentence_vec, keywords):
    """Return similarity of sentence to keywords of text"""
    #presumimibg for now that set of keywords as a whole is to be its own vector
    word_vec_list = []
    for word in keywords:
        word_vec = VECTOR_DICTIONARY[word]
        word_vec_list.append(word_vec)
    keywords_vector = sum_of_vectors(word_vec_list)
    return sentence_vec.similarity(keywords_vector)


def compute_centroid(sentences):
    """Centroid = arithimetic average over the coordinates of all sentence"""
    print('TO DO')

def sentence_2_centroid_cohesion(sentences):
    """Compute similiarity of s to centroid then normalise for all"""
    compute_centroid(sentences)

def senetence_2_sentence_cohesion(sentences):
    """Compute siimilarity between s and each other sentence then add up for s,
    then normalise for all"""
    print('TO DO')

def sentence_vector(sentence):
    """Will return vector which represents sentence"""
    word_vec_list = []
    for word in sentence:
        word_vec = VECTOR_DICTIONARY[word]
        word_vec_list.append(word_vec)
    return sum_of_vectors(word_vec_list)
