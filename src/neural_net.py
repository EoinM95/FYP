"""Functions and class for simulating a trainable ANN"""
import numpy as np
import tensorflow as tf #pylint: disable = E0401

LEARNING_RATE = 0.2
SEED = 1
MAX_TRAINING_ROUNDS = 100000
BATCH_SIZE = 200

class NeuralNetwork:
    """Class representing a trainable NeuralNetwork with one hidden layer"""
    def __init__(self, input_matrix, output_vector):
        self.input_matrix = input_matrix
        self.output_vector = output_vector
        self.input_nodes = input_matrix.shape[1]
        self.hidden_nodes = int((self.input_nodes + 1))
        self.input_2_hidden_synapse = tf.Variable(tf.random_normal([self.input_nodes,
                                                                    self.hidden_nodes], seed=SEED))
        self.hidden_2_output_synapse = tf.Variable(tf.random_normal([self.hidden_nodes,
                                                                     1], seed=SEED))
        self.input_placeholder = tf.placeholder(tf.float32, [None, self.input_nodes])
        self.output_placeholder = tf.placeholder(tf.float32, [None, 1])

        self.hidden_biases = tf.Variable(tf.random_normal([self.hidden_nodes],
                                                          seed=SEED))
        self.output_bias = tf.Variable(tf.random_normal([1], seed=SEED))
    def train(self):
        """Train neural net synapses by feeding forward then adjusting by back propagation"""
        hidden_layer = tf.add(tf.matmul(self.input_matrix,
                                        self.input_2_hidden_synapse), self.hidden_biases)
        hidden_layer = tf.nn.sigmoid(hidden_layer)
        output_layer = tf.matmul(hidden_layer,
                                 self.hidden_2_output_synapse) + self.output_bias
        cost_function, optimizer = self.build_cost_and_optimizer(output_layer)
        sess = tf.Session()
        tf.global_variables_initializer().run(session=sess)
        print('Starting training session')
        for epoch in range(MAX_TRAINING_ROUNDS):
            mean_error = 0
            total_batch = 1#int(self.input_matrix.shape[0]/BATCH_SIZE)
            for i in range(total_batch):
                batch_x, batch_y = self.batch_creator(i, BATCH_SIZE)
                f_dict = {self.input_placeholder: batch_x, self.output_placeholder: batch_y}
                _, cost = sess.run([optimizer, cost_function], feed_dict=f_dict)
                mean_error += cost / total_batch
            if epoch % 1000 == 0:
                print("Epoch:", (epoch), "cost =", "{:.5f}".format(mean_error), flush=True)
        print('Training complete')

    def build_cost_and_optimizer(self, output_layer):
        """Define and build tf variables representing cost/error function and
        training/optimizer function"""
        cost_function = 0.5 * tf.reduce_mean((output_layer - self.output_placeholder)
                                             * (output_layer - self.output_placeholder))
        #cost_function = tf.reduce_mean(
            #tf.nn.softmax_cross_entropy_with_logits(labels=self.output_placeholder,
            #                                        logits=output_layer))
        optimizer = tf.train.GradientDescentOptimizer(LEARNING_RATE).minimize(cost_function)
        return cost_function, optimizer


    def feed(self, input_matrix):
        """Calculate outputs for given input_matrix"""
        hidden_layer = tf.add(tf.matmul(self.input_matrix,
                                        self.input_2_hidden_synapse), self.hidden_biases)
        hidden_layer = tf.nn.relu(hidden_layer)
        output_layer = tf.matmul(hidden_layer,
                                 self.hidden_2_output_synapse) + self.output_bias
        sess = tf.Session()
        print(sess.run(output_layer, feed_dict={self.input_placeholder: input_matrix}))


    def batch_creator(self, batch_number, batch_size):
        """Create batch with random samples and return appropriate format"""
        start = batch_number * batch_size
        #end = (batch_number + 1) * batch_size
        batch_x = self.input_matrix[start:]#end
        batch_y = self.output_vector[start:]#end
        return batch_x, batch_y

def sigmoid(val, derivative=False):
    """Apply sigmoid function to every element of x"""
    if derivative is True:
        return val*(1-val)
    return 1/(1+np.exp(-val))
