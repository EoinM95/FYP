"""DocString for sentence_splitter """
import re
SENTENCE_PATTERN = r'(?<!..Mr|.Mrs|..Dr|Prof)\. (?=[A-Z])'
TOKEN_PATTERN = "(?<=[A-Za-z0-9]) "
def split(text):
    """Splits text into sentences, returns list"""
    return re.split(SENTENCE_PATTERN, text)

def tokenize(sentence):
    """Return list of tokens in sentence"""
    sentence = re.sub(r'(\.|[0-9]*)', '', sentence)
    sentence = re.sub(r'(\n|\r\n)', ' ', sentence)
    sentence = sentence.strip()
    return re.split(TOKEN_PATTERN, sentence.lower())

#print(split('Hello. World.'))
#print(split('This is a sentence. So is this.'))
#print(tokenize('This is a great example of what a sentence should look like.'))
