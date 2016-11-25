"""Defines Sentence Object"""
import re
from vector import Vector
from vector import sum_of_vectors
TOKEN_PATTERN = "[A-Za-z0-9]*( |,)"
class Sentence(object):
    """docSentstring for Sentence class."""
    def __init__(self, text):
        self.text = text
        self.s_vector = None
        self.tokens = None
        self.tokenize()
        self.vector()

    def vector(self):
        """Will return vector which represents sentence"""
        if  not self.s_vector:
            word_vec_list = []
            for word in self.tokenize():
                word_vec = Vector(word)
                word_vec_list.append(word_vec)
            self.s_vector = sum_of_vectors(word_vec_list)
        return self.s_vector


    def tokenize(self):
        """Return list of tokens in sentence"""
        if not self.tokens:
            self.tokens = re.split(self.text, TOKEN_PATTERN)
        return self.tokens
