"""Read in original texts and reference summaries from corpus"""
import xml.etree.ElementTree as ET
import re
from sentence_splitter import split
from utilities import DO_NOT_INCLUDE, score_threshold

HEADER_A_START = '<excludedsys'
HEADER_B_START = '<sysjudg_'

DOC_END = '</DOC>'
PUNCTUATION_PATTERN = r'([,\'\";&\-:\$%`/\\{}\*`_]|\.\.\.)'
PUNCTUATION_REGEX = re.compile(PUNCTUATION_PATTERN)
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
XML_ATT_PATTERN = r'([A-Z])=([0-9]+)'
XML_ATT_REGEX = re.compile(XML_ATT_PATTERN)
SQ_BRACKET_PATTERN = r'[\[\]]'
SQ_BRACKET_REGEX = re.compile(SQ_BRACKET_PATTERN)

def parse_from_new(filename):
    """Parse a novel document"""
    xml_tree = ET.parse(filename)
    root = xml_tree.getroot()
    title = root.find('title').text
    title = clean_input(title)
    doc_body = root.find('text').text
    doc_body = clean_input(doc_body)
    sentences = split(doc_body)
    return {'title':title, 'sentences': sentences}

def read_title_from_tipster_orig(filename):
    """Read in original text"""
    xml_string = ''
    with open(filename) as stream:
        for line in stream:
            line = SQ_BRACKET_REGEX.sub('\"', line)
            line = XML_AMP_REGEX.sub(r'&amp;', line)
            xml_string += line
    root = ET.fromstring(xml_string)
    title = find_title(root)
    return clean_input(title)



def read_from_tipster_scored(filename, tag_type='categ'):
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
                xml_string += line
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
        sentence['best_score'] = score_threshold(sentence['best_score'] / max_best_score)
        sentence['fixed_score'] = score_threshold(sentence['fixed_score'] / max_fixed_score)
    return sentences

def read_from_duc(filename):
    """Parse a training corpus text from a file"""
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
                line = XML_ATT_REGEX.sub(r'\1="\2"', line)
                xml_string += line
                if DOC_END in line:
                    doc_finished = True
    root = ET.fromstring(xml_string)
    sentences = []
    title = find_title(root)
    lead = root.find('LEADPARA')
    sentences += find_sentences(lead)
    main_body = root.find('TEXT')
    sentences += find_sentences(main_body)
    return {'title':title, 'sentences': sentences}

def find_sentences(tag):
    """Find all the sentences inside an XML tag"""
    sentences = []
    if tag is not None:
        for sentence_tag in tag.iter('s'):
            sentence = sentence_tag.text
            in_summary = sentence_tag.get('stype')
            if in_summary == '65537':
                in_summary = 1
            else:
                in_summary = 0
            sentences.append({'sentence': clean_input(sentence),
                              'in_summary': in_summary})
    return sentences

def find_title(root):
    """Find the document title"""
    title = ''
    title_nodes = root.findall('HEADLINE')
    if not title_nodes:
        title_nodes = root.findall('HEAD')
    if title_nodes:
        for node in title_nodes:
            for sentence_tag in node.iter('s'):
                title += sentence_tag.text
    else:
        title_nodes = root.findall('H3')
        if title_nodes:
            for node in title_nodes:
                for sentence_tag in node.iter('TI'):
                    title += sentence_tag.text
    if title == '':
        title = root.find('HL').text
        title = TITLE_DIVIDER_REGEX.split(title)
        title = title[0]
    return clean_input(title)

def clean_input(text):
    """Remove unnecessary chars from input"""
    return_text = text
    return_text = BRACKETS_REGEX.sub(' ', return_text)
    return_text = SENTENCE_END_REGEX.sub('.', return_text)
    return_text = WHITESPACE_REGEX.sub(' ', return_text)
    return_text = ABBREVIATION_REGEX.sub(r'\2\4\6', return_text)
    return_text = PUNCTUATION_REGEX.sub(' ', return_text)
    return_text = MULTIPLE_SPACES_REGEX.sub(' ', return_text)
    return return_text


if __name__ == '__main__':
    TEST_TEXT = '..\\duc01_tagged_meo_data\\d26e\\FBIS4-23474.S'
    #'..\\duc01_tagged_meo_data\\d36f\\AP890322-0078.S'
    #'..\\duc01_tagged_meo_data\\d01a\\SJMN91-06184003.S'
    PARSED = read_from_duc(TEST_TEXT)
    print('title = ', PARSED['title'])
    #PARSED_SENTENCES = PARSED['sentences']
    #for list_entry in PARSED_SENTENCES:
    #    print('sentence text = ', list_entry['sentence'])
    #    print('sentence in summary? ', list_entry['in_summary'])
