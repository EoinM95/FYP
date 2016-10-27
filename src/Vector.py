"""Defines vector class and accompanying helper functions"""
from math import sqrt
from scipy.spatial.distance import cosine
class Vector(object):
    """docSentstring for Vector class."""
    def __init__(self, coords):
        self.coords = coords
        self.size = len(coords)

    def norm(self):
        """Normalise vector"""
        sum_of_squares = 0
        for coord in self.coords:
            sum_of_squares += coord*coord
        return sqrt(sum_of_squares)

    def cosine_similarity(self, other):
        """Return cosine_similarity between 2 vectors"""
        return cosine(self.coords, other.coords)

    def sum(self, other):
        """Add two vectors"""
        new_coords = []
        for (coord1, coord2) in zip(self.coords, other.coords):
            print(coord1, coord2)
        return Vector(new_coords)

def sum_of_vectors(vector_list):
    """Add a list of vectors, return vector representing the sum"""
    sum_vector = vector_list[0]
    for i in range(1, len(vector_list())-1):
        sum_vector = vector_list[i].sum(sum_vector)
    return sum_vector
