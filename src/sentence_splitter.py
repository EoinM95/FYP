"""DocString for sentence_splitter """
import re
from sentence import Sentence
SENTENCE_PATTERN = "(?<=[^Mr|Mrs|Dr|Prof])\\. (?=[A-Z])"

def split(text):
    """Splits text into sentences, returns list"""
    return re.split(text, SENTENCE_PATTERN)

def create_sentence_objects(sentences):
    """Return list of sentece objects"""
    sentence_list = []
    for sentence in sentences:
        sentence_list.append(Sentence(sentence))
    return sentence_list

def read_sentences_from_file(filename):
    """Read in test file, clean file, split into sentences
        and return sentence objects"""
    file_contents = ' '
    with open(filename, encoding='utf8') as stream:
        file_contents = stream.read()
    file_contents = clean_input(file_contents)
    senteces = split(filename)
    return create_sentence_objects(senteces)

def clean_input(text):
    """Remove unnecessary chars from input"""
    print('Does nothing for now')
    return text
