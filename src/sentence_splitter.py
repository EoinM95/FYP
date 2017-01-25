"""DocString for sentence_splitter """
import re
SENTENCE_PATTERN = "(?<=[^Mr|Mrs|Dr|Prof])\\. (?=[A-Z])"
TOKEN_PATTERN = "[A-Za-z0-9]*( |,)"
def split(text):
    """Splits text into sentences, returns list"""
    return re.split(text, SENTENCE_PATTERN)

def tokenize(sentence):
    """Return list of tokens in sentence"""
    return re.split(sentence, TOKEN_PATTERN)
