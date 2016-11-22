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
        if len(self.coords) != len(other.coords):
            return "ERROR: Vectors not of same dimension"
        return 1 - cosine(self.coords, other.coords)

    def sum(self, other):
        """Add two vectors"""
        new_coords = []
        for (coord1, coord2) in zip(self.coords, other.coords):
            new_coords.append(coord1 + coord2)
        return Vector(new_coords)

def sum_of_vectors(vector_list):
    """Add a list of vectors, return vector representing the sum"""
    sum_vector = vector_list[0]
    for i in range(1, len(vector_list())-1):
        sum_vector = vector_list[i].sum(sum_vector)
    return sum_vector

COORDS_A = [1, 2, 3]
COORDS_B = [1, 2, 3]

VEC1 = Vector(COORDS_A)
VEC2 = Vector(COORDS_B)

# print('Cosine sim = ' + str(VEC1.cosine_similarity(VEC2)))
# VEC1.sum(VEC2)
