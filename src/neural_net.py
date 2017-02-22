"""Functions and classes for simulating a trainable ANN"""
import random
import numpy as np
import tensorflow as tf #pylint: disable = E0401

LEARNING_RATE = 0.1
SEED = 1
EPOCHS = 1000
BATCH_SIZE = 200

class NeuralNetwork:
    """Class representing a trainable NeuralNetwork with one hidden layer"""
    def __init__(self, input_matrix, output_vector):
        self.input_matrix = input_matrix
        self.output_vector = output_vector
        self.input_nodes = input_matrix.shape[1]
        self.hidden_nodes = self.input_nodes + 1
        self.tf_graph = TensorFlowGraph(self.input_nodes, self.hidden_nodes)

    def train(self):
        """Train neural net synapses by feeding forward then adjusting by back propagation"""
        print('Starting training session')
        for epoch in range(EPOCHS):
            mean_error = 0
            total_batch = int(self.input_matrix.shape[0]/BATCH_SIZE)
            if total_batch == 0:
                total_batch = 1
            for _ in range(total_batch):
                batch_x, batch_y = self.batch_creator(BATCH_SIZE)
                cost = self.tf_graph.run_with_cost(batch_x, batch_y)
                mean_error += cost / total_batch
            print("Epoch:", (epoch), "cost =", mean_error, flush=True)
        print('Training complete')

    def feed(self, input_matrix):
        """Calculate outputs for given input_matrix"""
        return self.tf_graph.run_for_output(input_matrix)

    def batch_creator(self, batch_size):
        """Create batch with random samples and return appropriate format"""
        dataset_size = self.input_matrix.shape[0]
        if batch_size > dataset_size:
            return self.input_matrix, self.output_vector
        sample = random.sample(range(dataset_size), batch_size)
        batch_x = []
        batch_y = []
        for index in sample:
            batch_x.append(self.input_matrix[index])
            batch_y.append(self.output_vector[index])
        batch_x = np.array(batch_x, dtype='float32')
        batch_y = np.array(batch_y, dtype='float32')
        return batch_x, batch_y


class TensorFlowGraph():
    """Wrapper class for TensorFlow libraries to build the computation graph
    and maintain a reference to the session and variables used for training """
    def __init__(self, input_nodes, hidden_nodes):
        self.synapses = build_synapses(input_nodes, hidden_nodes)
        self.input_placeholder = tf.placeholder(tf.float32, [None, input_nodes])
        self.output_placeholder = tf.placeholder(tf.float32, [None, 1])
        first_hidden_biases = tf.Variable(tf.random_normal([hidden_nodes]))
        second_hidden_biases = tf.Variable(tf.random_normal([int(hidden_nodes/2)]))
        output_bias = tf.Variable(tf.random_normal([1], seed=SEED))
        first_hidden_layer = tf.add(tf.matmul(self.input_placeholder,
                                              self.synapses['input_to_hidden']),
                                    first_hidden_biases)
        first_hidden_layer = tf.nn.sigmoid(first_hidden_layer)
        second_hidden_layer = tf.add(tf.matmul(first_hidden_layer,
                                               self.synapses['hidden_to_hidden']),
                                     second_hidden_biases)
        second_hidden_layer = tf.nn.sigmoid(second_hidden_layer)
        output_layer = tf.matmul(second_hidden_layer,
                                 self.synapses['hidden_to_output']) + output_bias
        self.output_layer = tf.nn.sigmoid(output_layer)
        cost_function, optimizer = self.build_cost_and_optimizer(self.output_layer)
        self.cost_function = cost_function
        self.optimizer = optimizer
        self.sess = tf.Session()
        tf.global_variables_initializer().run(session=self.sess)

    def build_cost_and_optimizer(self, output_layer):
        """Define and build tf variables representing cost/error function and
        training/optimizer function"""
        cost_function = tf.reduce_mean(tf.abs(self.output_placeholder - output_layer))
        optimizer = tf.train.AdamOptimizer(LEARNING_RATE).minimize(cost_function)
        return cost_function, optimizer

    def run_with_cost(self, inputs, outputs):
        """Run used for training, returns output of the cost_function"""
        f_dict = {self.input_placeholder: inputs, self.output_placeholder: outputs}
        _, cost = self.sess.run([self.optimizer, self.cost_function], feed_dict=f_dict)
        return cost

    def run_for_output(self, inputs):
        """Run used to generate output in evalutaion, returns output generated by network"""
        f_dict = {self.input_placeholder: inputs}
        output = self.sess.run(self.output_layer, feed_dict=f_dict)
        return output

def build_synapses(input_nodes, hidden_nodes):
    """Create variables representing synapses in the neural net"""
    input_to_hidden_1 = tf.Variable(tf.random_normal([input_nodes, hidden_nodes]))
    hidden_1_to_hidden_2 = tf.Variable(tf.random_normal([hidden_nodes, int(hidden_nodes/2)]))
    hidden_2_output = tf.Variable(tf.random_normal([int(hidden_nodes/2), 1]))
    return {'input_to_hidden': input_to_hidden_1,
            'hidden_to_hidden': hidden_1_to_hidden_2,
            'hidden_to_output': hidden_2_output}
