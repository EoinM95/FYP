"""Read in original texts and reference summaries from corpus"""
import xml.etree.ElementTree as ET
import re
from utilities import DO_NOT_INCLUDE

PUNCTUATION_PATTERN = r'[,\'\";&-:\$%`/\\{}\*]'
HEADER_A_START = '<excludedsys'
HEADER_B_START = '<sysjudg_'
PUNCTUATION_REGEX = re.compile(PUNCTUATION_PATTERN)
BRACKETED_KEYWORDS_PATTERN = r'\([A-Z]*\)'
BRACKETED_KEYWORDS_REGEX = re.compile(BRACKETED_KEYWORDS_PATTERN)
BRACKETS_PATTERN = r'[\(\)]'
BRACKETS_REGEX = re.compile(BRACKETS_PATTERN)
#replace U.S.A. with USA etc
ABBREVIATION_PATTERN = r'(([A-Za-z])\.)(([A-Za-z])\.)(([A-Za-z])\.)?'
ABBREVIATION_REGEX = re.compile(ABBREVIATION_PATTERN)
SENTENCE_END_PATTERN = r'(\!|\?)'
SENTENCE_END_REGEX = re.compile(SENTENCE_END_PATTERN)
TITLE_DIVIDER_PATTERN = r'\s----\s'
TITLE_DIVIDER_REGEX = re.compile(TITLE_DIVIDER_PATTERN)
MULTIPLE_SPACES_PATTERN = r'( )+'
MULTIPLE_SPACES_REGEX = re.compile(MULTIPLE_SPACES_PATTERN)
WHITESPACE_PATTERN = r'\s'
WHITESPACE_REGEX = re.compile(WHITESPACE_PATTERN)

XML_AMP_PATTERN = r'&(?!amp;)'
XML_AMP_REGEX = re.compile(XML_AMP_PATTERN)
SQ_BRACKET_PATTERN = r'[\[\]]'
SQ_BRACKET_REGEX = re.compile(SQ_BRACKET_PATTERN)

def parse_original_text(filename, style='wsj'):
    """Read in original text"""
    xml_string = ''
    with open(filename) as stream:
        for line in stream:
            line = SQ_BRACKET_REGEX.sub('\"', line)
            line = XML_AMP_REGEX.sub(r'&amp;', line)
            xml_string = xml_string + line
    root = ET.fromstring(xml_string)
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

    return {'text': clean_input(text, 'body'),
            'title': clean_input(title, 'title'),
            'has_keywords': has_keywords,
            'keywords': clean_input(keywords, 'keywords')}

def parse_scored_text(filename, tag_type='categ'):
    """Parse a scored summary of a text from a file"""
    xml_string = '<DOC>'
    header_lines = []
    with open(filename) as stream:
        for line in stream:
            if line.startswith(HEADER_A_START) or line.startswith(HEADER_B_START):
                header_lines.append(line)
            else:
                line = SQ_BRACKET_REGEX.sub('\"', line)
                line = XML_AMP_REGEX.sub(r'&amp;', line)
                xml_string = xml_string + line
    xml_string = xml_string + '</DOC>'
    root = ET.fromstring(xml_string)
    sentences = []
    max_best_score = 0
    max_fixed_score = 0
    for sentence_tag in root.findall('S'):
        sentence = sentence_tag.text
        best_score = sentence_tag.get('sys_'+tag_type+'_best')
        if best_score is None:
            best_score = 0
        else:
            best_score = len(best_score.split(','))
            if best_score > max_best_score:
                max_best_score = best_score
        fixed_score = sentence_tag.get('sys_'+tag_type+'_fixed')
        if fixed_score is None:
            fixed_score = 0
        else:
            fixed_score = len(fixed_score.split(','))
            if fixed_score > max_fixed_score:
                max_fixed_score = fixed_score
        sentences.append({'sentence': clean_input(sentence),
                          'best_score': best_score, 'fixed_score': fixed_score})

    if max_best_score == 0:
        return DO_NOT_INCLUDE
    for sentence in sentences:
        sentence['best_score'] = sentence['best_score'] / max_best_score
        sentence['fixed_score'] = sentence['fixed_score'] / max_fixed_score
    return sentences

def clean_input(text, section='body'):
    """Remove unnecessary chars from input"""
    return_text = text
    if section == 'title':
        text = TITLE_DIVIDER_REGEX.split(text)
        return_text = text[0]
    return_text = PUNCTUATION_REGEX.sub(' ', return_text)
    if section == 'keywords':
        return_text = BRACKETED_KEYWORDS_REGEX.sub('', return_text)
    else:
        return_text = BRACKETS_REGEX.sub(' ', return_text)
    return_text = SENTENCE_END_REGEX.sub('.', return_text)
    return_text = WHITESPACE_REGEX.sub(' ', return_text)
    return_text = ABBREVIATION_REGEX.sub(r'\2\4\6', return_text)
    return_text = MULTIPLE_SPACES_REGEX.sub(' ', return_text)
    return return_text
