"""Defines function to read vectors from file"""
import numpy
from vector import Vector
VECTOR_FILE = 'vectors.txt'

def read_vectors_from_file(filename=VECTOR_FILE):
    """Read vectors from file, return dictionary"""
    vec_dictionary = {}
    with open(filename, encoding='utf8') as stream:
        header = stream.readline()
        vocab_size, layer1_size = map(int, header.split())
        binary_len = numpy.dtype('float32').itemsize * layer1_size
        for i in range(vocab_size):
            word = []
            while True:
                char = stream.read(1)
                if char == ' ':
                    word = ''.join(word)
                    break
                if char != '\n':
                    word.append(char)
            vec_coords = numpy.fromstring(stream.read(binary_len), dtype='float32', count = layer1_size)
            next_vec = Vector(vec_coords)
            vec_dictionary[word] = next_vec
    return vec_dictionary


TEST = read_vectors_from_file()
print(TEST['the'].coords)
