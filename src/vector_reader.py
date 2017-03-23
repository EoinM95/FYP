"""Defines function to read vectors from file"""
import numpy as np
from utilities import show_progress
VECTOR_FILE = '../vectors.txt'

def read_word2vecs_from_file(filename=VECTOR_FILE):
    """Read vectors from file, return dictionary"""
    vec_dictionary = {}
    with open(filename, 'rb') as stream:
        header = stream.readline()
        vocab_size, vector_dimensions = map(int, header.split())
        binary_len = np.dtype('float32').itemsize * vector_dimensions
        print('Loading vector file containing: ', vocab_size, ' words')
        for i in range(vocab_size):
            percent_progress = int((i/vocab_size) * 100)
            show_progress(percent_progress)
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
            del string_bytes
            vec_coords = np.fromstring(stream.read(binary_len),
                                       dtype='float32', count=vector_dimensions)
            vec_dictionary[word] = vec_coords
    show_progress(100)
    return vec_dictionary

def save_test_vectors(input_vectors, output_vectors, input_filename, output_filename):
    """Save test vectors for reuse"""
    np.save(input_filename, input_vectors)
    np.save(output_filename, output_vectors)

def restore_test_vectors(input_file, output_file):
    """Restore input/output vectors for training"""
    try:
        input_vectors = np.load(input_file)
        output_vectors = np.load(output_file)
        return input_vectors, output_vectors
    except (IOError, ValueError):
        return None


#TEST = read_word2vecs_from_file()
#print(TEST['the'].coords)
