"""Test feature calculation"""
import unittest
import numpy as np
from features import compute_tf_isfs_for_text, similairty_to_title

class TestTSISFS(unittest.TestCase):
    """Test cases for tf_isf for text"""
    def test_2_sentence(self):
        """Basic 3 word/2 sentence test"""
        tokens_a = ['hello', 'world']
        tokens_b = ['goodbye', 'world']
        sentence_a = 'hello world'
        sentence_b = 'goodbye world'
        entry_a = {'sentence': sentence_a, 'tokens': tokens_a}
        entry_b = {'sentence': sentence_b, 'tokens': tokens_b}
        sentence_list = [entry_a, entry_b]
        ts_isfs = compute_tf_isfs_for_text(sentence_list)
        self.assertEqual(ts_isfs, [[1.0], [1.0]])


class TestTitleSim(unittest.TestCase):
    """Test cases for similairty_to_title"""
    def test_equal_vectors(self):
        """Test equal vectors have cosine sim of one"""
        sentence_vec = np.array([1, 2, 3])
        title_vector = np.array([1, 2, 3])
        sim = similairty_to_title(sentence_vec, title_vector)
        self.assertEqual(sim, 1)
