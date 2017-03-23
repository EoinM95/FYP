"""Class and functions to build a classifier"""
import numpy as np
from neural_net import NeuralNetwork
from nb_classifier import NBClassifier
from vector_reader import restore_test_vectors, save_test_vectors

INPUT_TEST_VECTORS_FILE = '../test_inputs.npy'
OUTPUT_TEST_VECTORS_FILE = '../test_outputs.npy'

NEURAL_NET = 1
NAIVE_BAYES = 0

class Classifier:
    """Wrapper class for Classifiers"""
    def __init__(self, classifier_type, sentence_features,
                 trained_model_file=None):
        self.classifier = None
        if trained_model_file is not None:
            self.load_model_from_file(classifier_type, sentence_features, trained_model_file)
        else:
            self.initialise_classifier(classifier_type, sentence_features)

    def initialise_classifier(self, classifier_type, sentence_features):
        """Restore classifier from file"""
        if classifier_type is NEURAL_NET:
            self.classifier = NeuralNetwork(sentence_features)
        else:
            self.classifier = NBClassifier() #pylint: disable = R0204

    def load_model_from_file(self, classifier_type, sentence_features, filename):
        """Restore classifier from file"""
        if classifier_type is NEURAL_NET:
            self.classifier = NeuralNetwork(sentence_features, filename)
        else:
            self.classifier = NBClassifier(filename) #pylint: disable = R0204

    def train(self, training_set):
        """Train classifier"""
        input_matrix, output_vector = training_set
        self.classifier.train(input_matrix, output_vector)

    def test(self, test_set):
        """Test and print precision, recall values"""
        input_matrix, expected_output = test_set
        correct = 0
        true_positives = 0
        false_positives = 0
        false_negatives = 0
        generated_output = self.classify(input_matrix)
        for i, output in enumerate(generated_output):
            expected = expected_output[i][0]
            output = round(output)
            if expected == output:
                correct += 1
            if expected == 1 and output == 1:
                true_positives += 1
            elif expected == 0 and output == 1:
                false_positives += 1
            elif expected == 1 and output == 0:
                false_negatives += 1
        success_rate = (correct / len(expected_output)) * 100
        precision = (true_positives / (true_positives + false_positives)) * 100
        recall = (true_positives / (true_positives + false_negatives)) * 100
        print('Success rate = ', success_rate, '%')
        print('Precision = ', precision, '%')
        print('Recall = ', recall, '%')
        save_test_vectors(input_matrix, expected_output,
                          INPUT_TEST_VECTORS_FILE, OUTPUT_TEST_VECTORS_FILE)

    def classify(self, input_matrix):
        """Classify inputs"""
        return self.classifier.feed(input_matrix)

    def save(self, filename):
        """Save classifier to file"""
        self.classifier.save(filename)

def build_and_test_classifier(classifier_type, sentence_features, processed_corpus):
    """Read in vectors, read in all scored summaries and corresponding originals for title+keywords
    Then calculate feature vectors for every sentence in every text"""
    training_set, test_set = train_and_test_split(processed_corpus)
    classifier = Classifier(classifier_type, sentence_features)
    classifier.train(training_set)
    classifier.test(test_set)
    if classifier_type is NEURAL_NET:
        classifier.save('./trained_model.tf')
    else:
        classifier.save('./bayes_model.nb')
    return classifier

def restore_and_test_classifier(classifier_type, sentence_features, trained_model_file):
    """Restore a classifier from a file and retest"""
    test_set = restore_test_vectors(INPUT_TEST_VECTORS_FILE, OUTPUT_TEST_VECTORS_FILE)
    classifier = Classifier(classifier_type, sentence_features, trained_model_file)
    classifier.test(test_set)
    return classifier

def train_and_test_split(processed_corpus):
    """Return balanced training set for negatives and positives, use rest as test data"""
    positive_inputs = []
    negative_inputs = []
    for corpus_entry in processed_corpus:
        feature_matrix = corpus_entry['feature_vectors']
        scores_vector = corpus_entry['scores_list']
        for i, feature_vector in enumerate(feature_matrix):
            score = scores_vector[i]
            if score[0] == 1:
                positive_inputs.append(feature_vector)
            else:
                negative_inputs.append(feature_vector)
    training_pos_size = int(len(positive_inputs)/2)
    training_inputs = []
    training_outputs = []
    test_inputs = []
    test_outputs = []
    for i, t_input in enumerate(positive_inputs):
        if i < training_pos_size:
            training_inputs.append(t_input)
            training_outputs.append([1])
        else:
            test_inputs.append(t_input)
            test_outputs.append([1])
    for i, t_input in enumerate(negative_inputs):
        if i < 2*training_pos_size:
            training_inputs.append(t_input)
            training_outputs.append([0])
        else:
            test_inputs.append(t_input)
            test_outputs.append([0])
    print('Training set contains ', training_pos_size, 'summary-worthy sentences, total size =',
          len(training_inputs))
    print('Test set contains ', len(test_inputs), 'sentences')
    training_inputs = np.array(training_inputs, dtype='float32')
    training_outputs = np.array(training_outputs, dtype='float32')
    test_inputs = np.array(test_inputs, dtype='float32')
    test_outputs = np.array(test_outputs, dtype='float32')
    return ((training_inputs, training_outputs), (test_inputs, test_outputs))
