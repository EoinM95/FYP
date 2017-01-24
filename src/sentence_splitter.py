"""DocString for sentence_splitter """
import re
SENTENCE_PATTERN = "(?<=[^Mr|Mrs|Dr|Prof])\\. (?=[A-Z])"
TOKEN_PATTERN = "[A-Za-z0-9]*( |,)"
def split(text):
    """Splits text into sentences, returns list"""
    return re.split(text, SENTENCE_PATTERN)

def read_sentences_from_file(filename):
    """Read in test file, clean file, split into sentences
        and return sentence objects"""
    file_contents = ' '
    with open(filename, encoding='utf8') as stream:
        file_contents = stream.read()
    file_contents = clean_input(file_contents)
    sentences = split(file_contents)
    return list(map(tokenize, sentences))

def clean_input(text):
    """Remove unnecessary chars from input"""
    print('Does nothing for now')
    return text

def tokenize(sentence):
    """Return list of tokens in sentence"""
    return re.split(sentence, TOKEN_PATTERN)
