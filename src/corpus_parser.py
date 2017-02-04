"""Read in original texts and reference summaries from corpus"""
import xml.etree.ElementTree as ET
import re


def parse_original_text(filename, style='wsj'):
    """Read in original text"""
    tree = ET.parse(filename)
    root = tree.getroot()
    text = root.find('TEXT').text
    title = ''
    has_keywords = True
    keywords = ''
    if style == 'wsj':
        title = root.find('HL').text
        in_node = root.find('IN')
        co_node = root.find('CO')
        has_keywords = not(in_node is None and co_node is None)
        if in_node is not None:
            keywords = in_node.text
        if co_node is not None:
            keywords = keywords + ' ' + co_node.text
    #Might just use wsj texts as they have keywords
    return {'text': clean_input(text, 'body'),
            'title': clean_input(title, 'title'),
            'has_keywords': has_keywords,
            'keywords': clean_input(keywords, 'keywords')}

def parse_scored_text(filename, style='wsj'):
    xml_string = '<DOC>'
    line_count = 0
    header_lines = []
    with open(filename) as stream:
        for line in stream:
            if line_count < 4:
                header_lines.append(line)
                line_count = line_count + 1
            else:
                xml_string = re.sub(r'[\[\]]', '\"', xml_string)
                xml_string = xml_string + line
    xml_string = xml_string + '</DOC>'
    root = ET.fromstring(xml_string)
    sentences = []
    for sentence_tag in root.findall('S'):
        sentence = sentence_tag.text
        best_score = sentence_tag.get('sys_categ_best')
        if best_score is None:
            best_score = 0
        else:
            best_score = len(best_score.split(','))
        fixed_score = sentence_tag.get('sys_categ_fixed')
        if fixed_score is None:
            fixed_score = 0
        else:
            fixed_score = len(fixed_score.split(','))
        sentences.append({'sentence': sentence,
                          'best_score': best_score, 'fixed_score': fixed_score})
    return sentences

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

#SCORED_TEST_FILE = '..\\composite_summaries\\tipster-composite-summaries\\categorization\\Global-Economy\\291\\docs\\WSJ900406-0086.sents.scored'
#SCORE_PARSED = parse_scored_text(SCORED_TEST_FILE)
#TEST_FILE = '..\\formal\\training\\formal-training\\categorization\\US-Foreign-Policy\\299\\docs\\WSJ911213-0036'
#PARSED = parse_original_text(TEST_FILE)
#print('title = ', PARSED['title'])
#print('text = ', PARSED['text'])
#print('keywords = ', PARSED['keywords'])
