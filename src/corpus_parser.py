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
    #Might just use wsj texts as they have keywords
    return {'text': clean_input(text, 'body'),
            'title': clean_input(title, 'title'),
            'keywords': clean_input(keywords, 'keywords')}


def clean_input(text, section='body'):
    """Remove unnecessary chars from input"""
    return_text = text
    if section == 'title':
        text = re.split(r'\s----\s', text)
        return_text = text[0]
    return_text = re.sub(r'(,|\'|\"|;|- )', ' ', return_text)
    if section == 'keywords':
        return_text = re.sub(r'\([A-Z]*\)', '', return_text)
    else:
        return_text = re.sub(r'\(', ' ', return_text)
        return_text = re.sub(r'\)', ' ', return_text)
    return_text = re.sub(r'(\!|\?)', '.', return_text)
    return_text = re.sub(r'\s', ' ', return_text)
    #replace U.S.A. with USA etc
    return_text = re.sub(r'(([A-Za-z])\.)(([A-Za-z])\.)(([A-Za-z])\.)?', r'\2\4\6', return_text)
    return_text = re.sub(r'( )+', ' ', return_text)
    return return_text


#TEST_FILE = '..\\formal\\training\\formal-training\\categorization\\US-Foreign-Policy\\299\\docs\\WSJ911213-0036'
#PARSED = parse_original_text(TEST_FILE)
#print('title = ', PARSED['title'])
#print('text = ', PARSED['text'])
#print('keywords = ', PARSED['keywords'])
