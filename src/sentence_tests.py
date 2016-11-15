"""Defines test classes for sentence_splitter"""
import unittest
from sentence_splitter import split

class TestSentence(unittest.TestCase):
    """Test class for sentence_splitter.py"""
    def test_split_simple(self):
        """Tests simplest case split, no curve balls"""
        text = "Automatic text processing is a research field that is currently\n\
        extremely active. One important task in this field is automatic summarization\n\
        which consists of reducing the size of a text while preserving its information content [9], [21]. A summarizer is a\n\
        system that produces a condensed representation of its input’s for user consumption\n\
        [12]. Summary construction is, in general, a complex task which ideally would involve\n\
        deep natural language processing capacities [15]. In order to simplify the problem,\n\
        current research is focused on extractive-summary generation [21]. An extractive\n\
        summary is simply a subset of the sentences of the original text. These summaries do\n\
        not guarantee a good narrative coherence, but they can conveniently represent an\n\
        approximate content of the text for relevance judgement."
        result = []
        self.assertEqual(result, split(text))
