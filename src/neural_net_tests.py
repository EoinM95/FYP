"""Tests for NeuralNetwork class"""
import unittest
import numpy as np

from neural_net import NeuralNetwork


class NeuralNetworkTests(unittest.TestCase):
    """Tests for NeuralNetwork class"""
    def test_xor_gate(self):
        """Simulate XOR gate and ensure working"""
        inputs = [[1.0, 1.0],
                  [1.0, 0.0],
                  [0.0, 1.0],
                  [0.0, 0.0]]
        output_vector = [[0.0],
                         [1.0],
                         [1.0],
                         [0.0]]
        inputs = np.array(inputs, dtype='float32')
        output_vector = np.array(output_vector)
        net = NeuralNetwork(inputs, output_vector)
        net.train()
        output = net.feed(np.array([[0, 1]], dtype='float32'))[0][0]
        output = round(output, 3)
        self.assertAlmostEqual(output, 1)
        output = net.feed(np.array([[1, 0]], dtype='float32'))[0][0]
        output = round(output, 3)
        self.assertAlmostEqual(output, 1)
        output = net.feed(np.array([[0, 0]], dtype='float32'))[0][0]
        output = round(output, 3)
        self.assertAlmostEqual(output, 0)
        output = net.feed(np.array([[1, 1]], dtype='float32'))[0][0]
        output = round(output, 3)
        self.assertAlmostEqual(output, 0)
