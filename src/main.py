"""Read a corpus, check there's a vector for everything"""

from vector_reader import read_vectors_from_file


VECTOR_FILE = '..\\GoogleNews-vectors-negative300.bin' #'..\\vectors.txt'

def main():
    vector_dictionary = load_vector_dictionary()
    print('User menu TODO')

def load_vector_dictionary():
    """Load vectors and return vector dictionary"""
    return read_vectors_from_file(VECTOR_FILE)


if __name__ == '__main__':
    main()
