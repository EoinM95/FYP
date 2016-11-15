"""Defines function to read vectors from file"""
from re import split
from vector import Vector
VECTOR_FILE = 'vec10_output.txt'

def read_vectors_from_file(filename=VECTOR_FILE):
    """Read vectors from file, return dictionary"""
    vec_dictionary = {}
    #with open(filename) as stream:
        #for line in stream:
    elements = split('hello 1 2 3', r'\s')
    word = elements[0]
    vec_coords = [float(i) for i in elements[1:]]
    next_vec = Vector(vec_coords)
    vec_dictionary[word] = next_vec
    return vec_dictionary

TEST = read_vectors_from_file()
for key, value in TEST.items():
    print(key, value)
