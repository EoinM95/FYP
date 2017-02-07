"""Tests for NeuralNetwork class"""
import unittest
import numpy as np

from neural_net import NeuralNetwork


class NeuralNetworkTests(unittest.TestCase):
    """Tests for NeuralNetwork class"""
    def test_xor_gate(self):
        """Simulate XOR gate and ensure working"""
        inputs = [[1, 1],
                  [1, 0],
                  [0, 1],
                  [0, 0]]
        output_vector = [[0],
                         [1],
                         [1],
                         [0]]
        inputs = np.array(inputs)
        output_vector = np.array(output_vector)
        net = NeuralNetwork(inputs, output_vector, input_nodes=2)
        for i in range(1000000):
            net.train()
        output = net.feed(np.array([0, 1, 1]))
        self.assertAlmostEqual(output[0], 1)
