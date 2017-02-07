"""Functions and class for simulating a trainable ANN"""
import numpy as np
LEARNING_RATE = 1
BIAS_TERM = 1
class NeuralNetwork:
    """Class representing a trainable NeuralNetwork with one hidden layer"""
    def __init__(self, input_matrix, output_vector, input_nodes=6):
        self.step_number = 0
        bias_terms = [[BIAS_TERM]] * input_matrix.shape[0]
        self.input_matrix = np.append(input_matrix, bias_terms, axis=1)
        self.output_vector = output_vector
        np.random.seed(1) #pylint: disable = E1101
        hidden_nodes = (input_nodes + 1) * 2
        self.input_to_hidden_synapse = 2*np.random.random((input_nodes + 1, hidden_nodes))-1
        self.hidden_2_output_synapse = 2*np.random.random((hidden_nodes, 1))-1

    def set_inputs_and_outputs(self, input_matrix, output_vector):
        """Set input and expected output for network"""
        self.input_matrix = input_matrix
        self.output_vector = output_vector

    def train(self):
        """Train neural net synapses by feeding forward then adjusting by back propagation"""
        hidden_layer = sigmoid(np.dot(self.input_matrix, self.input_to_hidden_synapse))
        output_layer = sigmoid(np.dot(hidden_layer, self.hidden_2_output_synapse))
        layer_2_error_matrix = self.output_vector - output_layer
        if self.step_number % 10000 == 0:
            print('Average error now at ', np.mean(np.abs(layer_2_error_matrix)), flush=True)
        layer_2_delta = layer_2_error_matrix * sigmoid(output_layer, derivative=True)
        layer_1_error_matrix = layer_2_delta.dot(self.hidden_2_output_synapse.T)
        layer_1_delta = layer_1_error_matrix * sigmoid(hidden_layer, derivative=True)
        self.hidden_2_output_synapse += hidden_layer.T.dot(layer_2_delta * LEARNING_RATE)
        self.input_to_hidden_synapse += self.input_matrix.T.dot(layer_1_delta * LEARNING_RATE)
        self.step_number += 1

    def feed(self, input_matrix):
        """Calculate outputs for given input_matrix"""
        hidden_layer = sigmoid(np.dot(input_matrix, self.input_to_hidden_synapse))
        output_layer = sigmoid(np.dot(hidden_layer, self.hidden_2_output_synapse))
        return output_layer

def sigmoid(val, derivative=False):
    """Apply sigmoid function to every element of x"""
    if derivative is True:
        return val*(1-val)
    return 1/(1+np.exp(-val))
