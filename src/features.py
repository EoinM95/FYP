"""Functions for calculating all the features for each sentence"""
from math import log2
from collections import Counter
from vector import Vector
import numpy as np

def calculate_feature_vectors(sentence_dict, title_vector, keywords_vector):
    """Calculate the normalised feature vector for every sentence"""
    return sentence_dict


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
            tf = sentence_word_counts[sentence][word] #pylint: disable = C0103
            num_of_s_containing_word = word_appearances[word]
            isf = log2(num_of_sentences/num_of_s_containing_word)
            word_tfisfs.append(tf*isf)
        sentence_results[sentence] = np.mean(np.array(word_tfisfs))
    #normalise for all
    return sentence_results


def similairty_to_title(sentence_vec, title_vector):
    """Return simliarity of sentence to the title"""
    return sentence_vec.similarity(title_vector)

def similairty_to_keywords(sentence_vec, keywords_vector):
    """Return similarity of sentence to keywords of text"""
    return sentence_vec.similarity(keywords_vector)


def compute_centroid(sentence_vectors):
    """Centroid = arithimetic average over the coordinates of all sentences"""
    super_vec = np.array(sentence_vectors)
    return Vector(np.mean(super_vec, axis=0))

def sentence_2_centroid_cohesion(sentence_vectors):
    """Compute similiarity of s to centroid then normalise for all"""
    centroid = compute_centroid(sentence_vectors)
    sim_vector = []
    for sentence in sentence_vectors:
        sim_vector.append(sentence.similiarity(centroid))


def senetence_2_sentence_cohesion(sentence_vectors):
    """Compute siimilarity between s and each other sentence then add up for s,
    then normalise for all"""
    cohesion_values = [0] * len(sentence_vectors)
    for i in range(len(sentence_vectors)-1):
        for j in range(i, len(sentence_vectors)):
            sim = sentence_vectors[i].similiarity(sentence_vectors[j])
            cohesion_values[i] = cohesion_values[i] + sim
            cohesion_values[j] = cohesion_values[j] + sim
    cohesion_values = np.array(cohesion_values)
    return  cohesion_values/ cohesion_values.max
