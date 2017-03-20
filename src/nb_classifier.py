"""Wrapper class and functions for scikit-learn NB classifier"""
from sklearn.externals import joblib #pylint: disable = E0401
from sklearn.naive_bayes import GaussianNB #pylint: disable = E0401

class NBClassifier():
    """Naive bayesian classifier"""
    def __init__(self, saved_model_file=None):
        self.classifier = None
        if saved_model_file is not None:
            self.classifier = joblib.load(saved_model_file)
        else:
            self.classifier = GaussianNB()
    def train(self, input_matrix, output_vector):
        """Train classifier"""
        output_vector = output_vector.flatten()
        self.classifier.fit(input_matrix, output_vector)

    def feed(self, input_matrix):
        """Predict class label"""
        return self.classifier.predict(input_matrix)

    def save(self, filename):
        """Save classifier to file"""
        joblib.dump(self.classifier, filename)
