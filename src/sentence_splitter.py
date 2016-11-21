"""DocString for sentence_splitter """
import re
SENTENCE_PATTERN = "(?<=[^Mr|Mrs|Dr|Prof])\\. (?=[A-Z])"

def split(text):
    """Splits text into sentences, returns list"""
    return re.split(text, SENTENCE_PATTERN)

#def cleanInput(text):
    #print('Does nothing for now')
    #re.remove

#def create_sentence_objects(listOfSentences):
    #return_list = []
    #for sentence in listOfSentences:
    #print('Will return list of Sentence objects')
TEXT = "Automatic text processing is a research field that is currently extremely active. One\n\
important task in this field is automatic summarization, which consists of reducing the\n\
size of a text while preserving its information content [9], [21]. A summarizer is a\n\
system that produces a condensed representation of its input’s for user consumption\n\
[12]. Summary construction is, in general, a complex task which ideally would involve\n\
deep natural language processing capacities [15]. In order to simplify the problem,\n\
current research is focused on extractive-summary generation [21]. An extractive\n\
summary is simply a subset of the sentences of the original text. These summaries do\n\
not guarantee a good narrative coherence, but they can conveniently represent an\n\
approximate content of the text for relevance judgement.\n\
A summary can be employed in an indicative way – as a pointer to some parts of\n\
the original document, or in an informative way – to cover all relevant information of\n\
the text [12]. In both cases the most important advantage of using a summary is its\n\
reduced reading time. Summary generation by an automatic procedure has also other\n\
advantages: (i) the size of the summary can be controlled; (ii) its content is\n\
determinist; and (iii) the link between a text element in the summary and its position\n\
in the original text can be easily established."
print(split(TEXT))
