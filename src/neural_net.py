"""Functions and class for simulating a trainable ANN"""
import numpy as np
import tensorflow as tf #pylint: disable = E0401

LEARNING_RATE = 1
SEED = 1
MAX_TRAINING_ROUNDS = 10
BATCH_SIZE = 200

class NeuralNetwork:
    """Class representing a trainable NeuralNetwork with one hidden layer"""
    def __init__(self, input_matrix, output_vector):
        self.input_matrix = input_matrix
        self.output_vector = output_vector
        self.input_nodes = input_matrix.shape[1]
        self.hidden_nodes = int((self.input_nodes + 1) / 2)

    def set_inputs_and_outputs(self, input_matrix, output_vector):
        """Set input and expected output for network"""
        self.input_matrix = input_matrix
        self.output_vector = output_vector

    def train(self):#pylint: disable = R0914
        """Train neural net synapses by feeding forward then adjusting by back propagation"""
        input_placeholder = tf.placeholder(tf.float32, [None, self.input_nodes])
        output_placeholder = tf.placeholder(tf.float32, [None, 1])
        input_2_hidden_synapse = tf.Variable(tf.random_normal([self.input_nodes,
                                                               self.hidden_nodes], seed=SEED))
        hidden_2_output_synapse = tf.Variable(tf.random_normal([self.hidden_nodes,
                                                                1], seed=SEED))
        hidden_biases = tf.Variable(tf.random_normal([self.hidden_nodes],
                                                     seed=SEED))
        output_biases = tf.Variable(tf.random_normal([1], seed=SEED))
        hidden_layer = tf.add(tf.matmul(self.input_matrix,
                                        input_2_hidden_synapse), hidden_biases)
        hidden_layer = tf.nn.relu(hidden_layer)
        output_layer = tf.matmul(hidden_layer,
                                 hidden_2_output_synapse) + output_biases
        cost_function = tf.reduce_mean(
            tf.nn.softmax_cross_entropy_with_logits(logits=output_layer,
                                                    labels=self.output_vector))
        optimizer = tf.train.AdamOptimizer(learning_rate=LEARNING_RATE).minimize(cost_function)
        init = tf.global_variables_initializer()
        sess = tf.Session()
        sess.run(init)
        print('Starting training session')
        for epoch in range(MAX_TRAINING_ROUNDS):
            mean_error = 0
            total_batch = int(self.input_matrix.shape[0]/BATCH_SIZE)
            for i in range(total_batch):
                batch_x, batch_y = self.batch_creator(i, BATCH_SIZE)
                _, cost = sess.run(optimizer,
                                   feed_dict={input_placeholder: batch_x,
                                              output_placeholder: batch_y})
                mean_error += cost/total_batch
            print("Epoch:", (epoch+1), "cost =", "{:.5f}".format(mean_error))
        print('Training complete')


    def feed(self, input_matrix):
        """Calculate outputs for given input_matrix"""
        print('TO DO')

    def batch_creator(self, batch_number, batch_size):
        """Create batch with random samples and return appropriate format"""
        start = batch_number * batch_size
        end = (batch_number + 1) * batch_size
        batch_x = self.input_matrix[start:end]
        batch_y = self.input_matrix[start:end]
        return batch_x, batch_y

def sigmoid(val, derivative=False):
    """Apply sigmoid function to every element of x"""
    if derivative is True:
        return val*(1-val)
    return 1/(1+np.exp(-val))