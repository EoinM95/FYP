"""Functions for calculating all the features for each sentence"""
from math import log2
from collections import Counter
from scipy.spatial.distance import cosine
import numpy as np

#feature_vec = [tf*isf, sim_to_title, centroid_cohesion, sentence_cohesion, sim_to_keywords]
def calculate_feature_vectors(sentence_list, title_vector, keywords_vector):
    """Calculate the normalised feature vector for every sentence"""
    feature_vectors = compute_tf_isfs_for_text(sentence_list)
    sentence_vectors = []
    for sentence in sentence_list:
        sentence_vectors.append(sentence['sentence_vec'])
    centroid_cohesion_values = sentence_2_centroid_cohesion(sentence_vectors)
    sentence_cohesion_values = senetence_2_sentence_cohesion(sentence_vectors)
    for i, sentence_vector in enumerate(sentence_vectors):
        feature_vector = np.array(feature_vectors[i])
        sim_to_title = similairty_to_title(sentence_vector, title_vector)
        feature_vector = np.append(feature_vector, values=sim_to_title)
        centroid_cohesion = centroid_cohesion_values[i]
        feature_vector = np.append(feature_vector, values=centroid_cohesion)
        sentence_cohesion = sentence_cohesion_values[i]
        feature_vector = np.append(feature_vector, values=sentence_cohesion)
        sim_to_keywords = similairty_to_keywords(sentence_vector, keywords_vector)
        feature_vector = np.append(feature_vector, values=sim_to_keywords)
        position = i/len(sentence_vectors)
        feature_vector = np.append(feature_vector, values=position)
        feature_vectors[i] = feature_vector
    return np.array(feature_vectors)

def compute_tf_isfs_for_text(sentence_list):
    """Compute the mean term frequency*inverse sentence frequency for
    all words of sentence, for every sentence. Analagous to tf*idf"""
    sentence_results = []
    num_of_sentences = len(sentence_list)
    sentence_word_counts = {}
    word_appearances = {}
    for sentence_entry in sentence_list:
        sentence = sentence_entry['sentence']
        tokens = sentence_entry['tokens']
        word_counter = Counter(tokens)
        sentence_word_counts[sentence] = word_counter
        for word in word_counter.keys():
            word_appearances[word] = word_appearances.get(word, 0) + 1
    for sentence_entry in sentence_list:
        word_tfisfs = []
        sentence = sentence_entry['sentence']
        tokens = sentence_entry['tokens']
        for word in tokens:
            tf = sentence_word_counts[sentence][word] #pylint: disable = C0103
            num_of_s_containing_word = word_appearances[word]
            isf = log2(num_of_sentences/num_of_s_containing_word)
            word_tfisfs.append(tf*isf)
        sentence_results.append([np.mean(np.array(word_tfisfs))])
    results = np.array(sentence_results)
    return (results / results.max(axis=0)).tolist() #pylint: disable = E1101


def similairty_to_title(sentence_vec, title_vector):
    """Return simliarity of sentence to the title"""
    return similarity(sentence_vec, title_vector)

def similairty_to_keywords(sentence_vec, keywords_vector):
    """Return similarity of sentence to keywords of text"""
    return similarity(sentence_vec, keywords_vector)


def compute_centroid(sentence_vectors):
    """Centroid = arithimetic average over the coordinates of all sentences"""
    super_vec = np.array(sentence_vectors)
    return np.mean(super_vec, axis=0)

def sentence_2_centroid_cohesion(sentence_vectors):
    """Compute similiarity of s to centroid then normalise for all"""
    centroid = compute_centroid(sentence_vectors)
    sim_vector = []
    for sentence in sentence_vectors:
        sim_vector.append(similarity(sentence, centroid))
    sim_vector = np.array(sim_vector)
    return  sim_vector/sim_vector.max() #pylint: disable = E1101

def similarity(vec1, vec2):
    """Return cosine_similarity between 2 vectors"""
    if vec1.size != vec2.size:
        return "ERROR: Vectors not of same dimension"
    return 1 - cosine(vec1, vec2)


def senetence_2_sentence_cohesion(sentence_vectors):
    """Compute siimilarity between s and each other sentence then add up for s,
    then normalise for all"""
    cohesion_values = [0] * len(sentence_vectors)
    for i in range(len(sentence_vectors)-1):
        for j in range(i, len(sentence_vectors)):
            sim = similarity(sentence_vectors[i], sentence_vectors[j])
            cohesion_values[i] += sim
            cohesion_values[j] += sim
    cohesion_values = np.array(cohesion_values)
    return  cohesion_values/cohesion_values.max()
