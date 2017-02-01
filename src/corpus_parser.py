"""Read in original texts and reference summaries from corpus"""
import xml.etree.ElementTree as ET
import re


def parse_original_text(filename, style='wsj'):
    """Read in original text"""
    tree = ET.parse(filename)
    root = tree.getroot()
    text = root.find('TEXT').text
    title = ''
    keywords = ''
    if style == 'wsj':
        title = root.find('HL').text
        keywords = root.find('IN').text
    return {'text': clean_input(text, 'body', style),
            'title': clean_input(title, 'title', style),
            'keywords': clean_input(keywords, 'keywords', style)}


def clean_input(text, section='body', style='wsj'):
    """Remove unnecessary chars from input"""
    return_text = text
    if section == 'title':
        if style == 'wsj':
            text = re.split(r'\s----\s', text)
            print(text)
            return_text = text[0]
    return return_text

PARSED = parse_original_text('C:\\Users\\eoinm\\FYP\\formal\\training\\formal-training\\categorization\\US-Foreign-Policy\\299\\docs\\WSJ911213-0036')
print('title = ', PARSED['title'])
#print('text = ', PARSED['text'])
#print('keywords = ', PARSED['keywords'])
