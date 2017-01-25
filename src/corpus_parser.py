"""Read in original texts and reference summaries from corpus"""
import xml.etree.ElementTree as ET
#import re


def parse_original_text(filename):
    """Read in original text"""
    tree = ET.parse(filename)
    root = tree.getroot()
    text = root.find('TEXT').text
    title = root.find('HL').text
    return {'text': text, 'title': title}


def clean_input(text):
    """Remove unnecessary chars from input"""
    print('Does nothing for now')
    return text

parse_original_text('C:\\Users\\eoinm\\FYP\\formal\\training\\formal-training\\categorization\\US-Foreign-Policy\\299\\docs\\WSJ911213-0036')
