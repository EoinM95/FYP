"""Defines Sentence Object"""
from vector import Vector
from vector import sum_of_vectors
class Sentence(object):
    """docSentstring for Sentence class."""
    def __init__(self, text):
        self.text = text

    def sentence_vector(self):
        """Will return vector which represents sentence"""
        word_vec_list = []
        for word in self.text:
            word_vec = Vector(word)
            word_vec_list.append(word_vec)
        return sum_of_vectors(word_vec_list)
    
