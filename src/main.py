"""Read a corpus, check there's a vector for everything"""

from vector_reader import read_vectors_from_file
from summariser import build_summariser
from classifier import NEURAL_NET, NAIVE_BAYES

VECTOR_FILE = '..\\GoogleNews-vectors-negative300.bin' #'..\\vectors.txt'
TRAINED_NEURAL_NET_FILE = './trained_model.tf'
TRAINED_NAIVE_BAYES_FILE = './bayes_model.nb'


def main():
    """Main program, provide user menu for summariser"""
    print('In order for summariser to work a word2vec vector file needs to be loaded')
    print('Loading default word2vec file')
    vector_dictionary = load_vector_dictionary()
    summariser = top_level_user_menu(vector_dictionary)
    if summariser is not None:
        summariser_options_menu(summariser)

def load_vector_dictionary():
    """Load vectors and return vector dictionary"""
    return read_vectors_from_file(VECTOR_FILE)

def top_level_user_menu(vector_dictionary):
    """First level user menu"""
    summariser = None
    finished = True
    while not finished:
        print('Welcome! From here you can type')
        print('nn to use the pre-trained neural net based summariser')
        print('nb to use the pre-trained naive bayes based summariser')
        print('tr to start training a new summariser or retraining a previously saved one')
        print('q to quit the program')
        user_choice = input('Enter your selection here')
        if user_choice == 'nn':
            summariser = build_summariser(vector_dictionary, NEURAL_NET, TRAINED_NEURAL_NET_FILE)
        elif user_choice == 'nb':
            summariser = build_summariser(vector_dictionary, NAIVE_BAYES, TRAINED_NAIVE_BAYES_FILE)
        elif user_choice == 'tr':
            train_new_menu(vector_dictionary)
        elif user_choice == 'q':
            print('Program will now exit, goodbye!')
            finished = True
    return summariser

def summariser_options_menu(summariser):
    """User menu for summarising documents with trained summariser"""
    print('TODO')

def train_new_menu(vector_dictionary):
    """User menu for creating a new summariser"""
    print('TODO')

if __name__ == '__main__':
    main()
