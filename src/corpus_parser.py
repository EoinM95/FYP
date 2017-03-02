"""Read in original texts and reference summaries from corpus"""
import xml.etree.ElementTree as ET
import re
#from utilities import DO_NOT_INCLUDE

PUNCTUATION_PATTERN = r'[,\'\";&-:\$%`/\\{}\*]'
DOC_END = '</DOC>'
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

def read_parsed(filename):
    """Parse a scored summary of a text from a file"""
    xml_string = ''
    header_lines = []
    term_lines = []
    line_count = 0
    header_line_num = 3
    doc_finished = False
    with open(filename) as stream:
        for line in stream:
            if line_count < header_line_num:
                header_lines.append(line)
                line_count += 1
            elif doc_finished:
                term_lines.append(line)
            else:
                line = XML_AMP_REGEX.sub(r'&amp;', line)
                xml_string += line
                if DOC_END in line:
                    doc_finished = True
    print(xml_string)
    root = ET.fromstring(xml_string)
    sentences = []
    title = root.find('HEADLINE').text
    lead = root.find('LEADPARA')
    main_body = root.find('TEXT')
    for sentence_tag in main_body.iter('s'):
        sentence = sentence_tag.text
        position = sentence_tag.get('num')
        in_summary = sentence_tag.get('stype')
        in_summary = bool(in_summary == '65537')
        sentences.append({'sentence': clean_input(sentence),
                          'position': position,
                          'in_summary': in_summary})
    return {'title':title, 'sentences': sentences}

def find_sentences(tag):
    for sentence_tag in tag.iter('s'):
        sentence = sentence_tag.text
        position = sentence_tag.get('num')
        in_summary = sentence_tag.get('stype')
        in_summary = bool(in_summary == '65537')
        sentences.append({'sentence': clean_input(sentence),
                          'position': position,
                          'in_summary': in_summary})


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
test_text = '..\\duc01_tagged_meo_data\\d01a\\SJMN91-06184003.S'
parsed = read_parsed(test_text)
print('title = ', parsed['title'])
parsed_sentences = parsed['sentences']
for list_entry in parsed_sentences:
    print('sentence text = ', list_entry['sentence'])
    print('sentence in summary? ', list_entry['in_summary'])
