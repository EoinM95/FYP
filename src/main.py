"""Main program, show user menu, provide options to load or build summariser
    and provide options to summarise texts"""
import os
from vector_reader import read_word2vecs_from_file
from summariser import build_summariser, find_sample_files_and_summarise
from classifier import NEURAL_NET, NAIVE_BAYES

VECTOR_FILE = '../GoogleNews-vectors-negative300.bin' #'../vectors.txt'
TRAINED_NEURAL_NET_FILE = '../trained_NNs/trained_model.tf'
TRAINED_NAIVE_BAYES_FILE = '../trained_bayes/bayes_model.nb'


def main():
    """Main program, provide user menu for summariser"""
    print('In order for summariser to work a word2vec vector file needs to be loaded', flush=True)
    print('Loading default word2vec file', flush=True)
    vector_dictionary = load_vector_dictionary()
    summariser = top_level_user_menu(vector_dictionary)
    if summariser is not None:
        summariser_options_menu(summariser)

def load_vector_dictionary():
    """Load vectors and return vector dictionary"""
    return read_word2vecs_from_file(VECTOR_FILE)

def top_level_user_menu(vector_dictionary):
    """First level user menu"""
    summariser = None
    finished = False
    while not finished:
        print('Welcome! From here you can type', flush=True)
        print('nn to use the pre-trained neural net based summariser', flush=True)
        print('nb to use the pre-trained naive bayes based summariser', flush=True)
        print('tr to start training a new summariser or retraining a previously saved one',
              flush=True)
        print('q to quit the program', flush=True)
        user_choice = input('Enter your selection here: ')
        if user_choice == 'nn':
            summariser = build_summariser(vector_dictionary, NEURAL_NET, TRAINED_NEURAL_NET_FILE)
            finished = True
        elif user_choice == 'nb':
            summariser = build_summariser(vector_dictionary, NAIVE_BAYES, TRAINED_NAIVE_BAYES_FILE)
            finished = True
        elif user_choice == 'tr':
            summariser = train_new_menu(vector_dictionary)
            finished = True
        elif user_choice == 'q':
            print('Program will now exit, goodbye!', flush=True)
            summariser = None
            finished = True
        else:
            print('Input not recognised, could you try that again?', flush=True)
    return summariser

def summariser_options_menu(summariser):
    """User menu for summarising documents with trained summariser"""
    finished = False
    print('You now have a working summariser!', flush=True)
    while not finished:
        print('From here you can enter a file to summarise and a filename to write the summary to',
              flush=True)
        print('You can also type ALL into the summary file prompt')
        print(' which will summarise all the sample documents.')
        print('Sample summaries will be written to ../sample_summaries')
        print('****Warning this will overwrite whatever was in the previous set of samples***')
        print('Or type q into the summary file to quit the program', flush=True)
        file_to_summarise = input('Enter the file to summarise here: ')
        if file_to_summarise == 'q':
            print('Program will now exit, goodbye!', flush=True)
            summariser = None
            finished = True
        elif file_to_summarise == 'ALL':
            find_sample_files_and_summarise(summariser)
        elif os.path.isfile(file_to_summarise):
            output_file = input('Enter the file to write the summary to here: ')
            success = summariser.summarise(file_to_summarise, output_file)
            if success:
                print('Summary successfully written to ', output_file)
            else:
                print('An error occurred while parsing this document, try another?')
        else:
            print('File to summarise could not be found, could you try that again?')

def train_new_menu(vector_dictionary):
    """User menu for creating a new summariser"""
    finished = False
    while not finished:
        print('Let\'s start training a new classifier for your summariser! From here you can type',
              flush=True)
        print('nn to train a new neural net based on the default corpus', flush=True)
        print('nb to a new naive bayes classifier based on the default corpus', flush=True)
        print('q to quit the program', flush=True)
        user_choice = input('Enter your selection here: ')
        if user_choice == 'nn':
            summariser = build_summariser(vector_dictionary, NEURAL_NET, TRAINED_NEURAL_NET_FILE)
            finished = True
        elif user_choice == 'nb':
            summariser = build_summariser(vector_dictionary, NAIVE_BAYES, TRAINED_NAIVE_BAYES_FILE)
            finished = True
        elif user_choice == 'q':
            print('Program will now exit, goodbye!', flush=True)
            summariser = None
            finished = True
        else:
            print('Input not recognised, could you try that again?', flush=True)
    return summariser

if __name__ == '__main__':
    main()
