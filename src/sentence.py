"""Defines Sentence Object"""
import re
from vector import Vector
from vector import sum_of_vectors
TOKEN_PATTERN = "[A-Za-z0-9]*( |,)"
class Sentence(object):
    """docSentstring for Sentence class."""
    def __init__(self, text):
        self.text = text

    def sentence_vector(self):
        """Will return vector which represents sentence"""
        word_vec_list = []
        for word in self.tokenize():
            word_vec = Vector(word)
            word_vec_list.append(word_vec)
        return sum_of_vectors(word_vec_list)

    def tokenize(self):
        """Return list of tokens in sentence"""
        return re.split(self.text, TOKEN_PATTERN)
