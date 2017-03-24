"""Test feature calculation"""
import unittest
import numpy as np
from features import compute_tf_isfs_for_text, similairty_to_title, similairty_to_keywords
from main import sentence_vector
from vector_reader import read_word2vecs_from_file

SMALL_VECTOR_FILE = '../vectors.txt'

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


class TestSimFunctions(unittest.TestCase):
    """Test cases for similairty_to_title"""
    def test_equal_vectors(self):
        """Test equal vectors have cosine sim of one"""
        vec_a = np.array([1, 2, 3])
        vec_b = np.array([1, 2, 3])
        sim_title = similairty_to_title(vec_a, vec_b)
        sim_keyword = similairty_to_keywords(vec_a, vec_b)
        self.assertEqual(sim_title, 1)
        self.assertEqual(sim_keyword, 1)

    def test_equal_from_words(self):
        """Test two equal sentences have cosine sim of one"""
        vector_dictionary = read_word2vecs_from_file(SMALL_VECTOR_FILE)
        sentence = ['hello', 'world']
        vec_a = sentence_vector(sentence, vector_dictionary)
        vec_b = sentence_vector(sentence, vector_dictionary)
        sim_title = similairty_to_title(vec_a, vec_b)
        sim_keyword = similairty_to_keywords(vec_a, vec_b)
        self.assertAlmostEqual(sim_title, 1.0)
        self.assertAlmostEqual(sim_keyword, 1.0)
