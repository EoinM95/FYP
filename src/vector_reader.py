"""Defines function to read vectors from file"""
import numpy as np
from vector import Vector
VECTOR_FILE = 'vectors.txt'

def read_vectors_from_file(filename=VECTOR_FILE):
    """Read vectors from file, return dictionary"""
    vec_dictionary = {}
    with open(filename, 'rb') as stream:
        header = stream.readline()
        vocab_size, layer1_size = map(int, header.split())
        binary_len = np.dtype('float32').itemsize * layer1_size
        print(vocab_size, layer1_size, binary_len)
        for i in range(vocab_size):
            string_bytes = bytearray()
            while True:
                next_byte = stream.read(1)
                try:
                    char = next_byte.decode('utf8')
                except UnicodeDecodeError:
                    string_bytes += bytearray(next_byte)
                    continue
                if char == ' ':
                    word = string_bytes.decode('utf8')
                    break
                if char != '\n':
                    string_bytes += bytearray(next_byte)
            vec_coords = np.fromstring(stream.read(binary_len), dtype='float32', count=layer1_size)
            next_vec = Vector(vec_coords)
            vec_dictionary[word] = next_vec
    return vec_dictionary


TEST = read_vectors_from_file()
print(TEST['the'].coords)
