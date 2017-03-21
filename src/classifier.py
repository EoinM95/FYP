"""Class and functions to build a classifier"""
import numpy as np
from neural_net import NeuralNetwork
from nb_classifier import NBClassifier

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

    def classify(self, input_matrix):
        """Classify inputs"""
        return self.classifier.feed(input_matrix)

    def save(self, filename):
        """Save classifier to file"""
        self.classifier.save(filename)

def build_and_test_classifier(classifier_type, sentence_features, training_corpus,
                              test_corpus, trained_model_file):
    """Read in vectors, read in all scored summaries and corresponding originals for title+keywords
    Then calculate feature vectors for every sentence in every text"""
    training_set = create_input_output_vecs(training_corpus)
    test_set = create_input_output_vecs(test_corpus)
    classifier = Classifier(classifier_type, sentence_features, trained_model_file)
    if trained_model_file is None:
        classifier.train(training_set)
    classifier.test(test_set)
    if trained_model_file is None:
        if classifier_type is NEURAL_NET:
            classifier.save('./trained_model.tf')
        else:
            classifier.save('./bayes_model.nb')
    return classifier

def create_input_output_vecs(processed_corpus):
    """Turn list into two seperate lists of inputs and outputs"""
    inputs = []
    outputs = []
    positives = 0
    for corpus_entry in processed_corpus:
        feature_matrix = corpus_entry['feature_vectors']
        scores_vector = corpus_entry['scores_list']
        for i, feature_vector in enumerate(feature_matrix):
            score = scores_vector[i]
            if score[0] == 1:
                positives += 1
            inputs.append(feature_vector)
            outputs.append(score)
    print('Set contains ', positives, 'summary-worthy sentences, total size =',
          len(inputs))
    inputs = np.array(inputs, dtype='float32')
    outputs = np.array(outputs, dtype='float32')
    return (inputs, outputs)
