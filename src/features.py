"""Functions for calculating all the features for each sentence"""
from math import log2
from collections import Counter
from vector import Vector
import numpy as np
#feature_vec = [tf*isf, sim_to_title, sim_to_keywords, centroid_cohesion, sentence_cohesion]
def calculate_feature_vectors(sentence_dict, title_vector, keywords_vector):
    """Calculate the normalised feature vector for every sentence"""
    feature_vectors = compute_tf_isfs_for_text(sentence_dict)
    sentence_list = sentence_dict.keys()
    sentence_vectors = []
    for i in range(len(sentence_list)):
        sentence = sentence_list[i]
        sentence_vectors.append(sentence_dict[sentence]['sentence_vec'])
    centroid_cohesion_values = sentence_2_centroid_cohesion(sentence_vectors)
    sentence_cohesion_values = senetence_2_sentence_cohesion(sentence_vectors)
    for i in range(len(sentence_vectors)):
        sentence_vector = sentence_vectors[i]
        feature_vector = feature_vectors[i]
        feature_vector.append(similairty_to_title(sentence_vector, title_vector))
        feature_vector.append(similairty_to_keywords(sentence_vector, keywords_vector))
        feature_vector.append(centroid_cohesion_values[i])
        feature_vector.append(sentence_cohesion_values[i])
        feature_vectors[i] = feature_vector
    return feature_vectors    

def compute_tf_isfs_for_text(sentence_dict):
    """Compute the mean term frequency*inverse sentence frequency for
    all words of sentence, for every sentence. Analagous to tf*idf"""
    sentence_results = np.array()
    num_of_sentences = len(sentence_dict)
    sentence_word_counts = {}
    word_appearances = {}
    for sentence in sentence_dict.keys():
        word_counter = Counter(sentence['tokens'])
        sentence_word_counts[sentence] = word_counter
        for word in word_counter.keys():
            word_appearances[word] = word_appearances.get(word, default=0) + 1
    for sentence in sentence_dict.keys():
        word_tfisfs = []
        for word in sentence['tokens']:
            tf = sentence_word_counts[sentence][word] #pylint: disable = C0103
            num_of_s_containing_word = word_appearances[word]
            isf = log2(num_of_sentences/num_of_s_containing_word)
            word_tfisfs.append(tf*isf)
        sentence_results.append([np.mean(np.array(word_tfisfs))])
    return sentence_results / sentence_results.max(axis=0)


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
    sim_vector = np.array()
    for sentence in sentence_vectors:
        sim_vector.append(sentence.similiarity(centroid))
    sim_vector = np.array(sim_vector)
    return  sim_vector/sim_vector.max


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
    return  cohesion_values/cohesion_values.max
