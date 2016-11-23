"""Tests the Vectors class """
import unittest
import numpy as np
from vector import Vector
class VectorTest(unittest.TestCase):
    """Vector test case"""
    def test_add(self):
        """Test addition of two vectors"""
        a_vec = Vector([1, 2, 3])
        b_vec = Vector([1, 2, 3])
        result = a_vec.add(b_vec)
        self.assertTrue(np.array_equal(result.coords, [2, 4, 6]))
