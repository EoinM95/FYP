"""Read in original texts and reference summaries from corpus"""
import xml.etree.ElementTree as ET
import re
from utilities import DO_NOT_INCLUDE

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
IN_TEXT_ATTRIBUTES_PATTERN = r'\<F.*\/?>'
IN_TEXT_ATTRIBUTES_REGEX = re.compile(IN_TEXT_ATTRIBUTES_PATTERN)
SQ_BRACKETS_PATTERN = r'\[.*\]'
SQ_BRACKETS_REGEX = re.compile(SQ_BRACKETS_PATTERN)
TEXT_STARTER = '[Text]'
TEXT_STARTER_PATTERN = r'(<TEXT>)(.*\[Text\]) (.*)'
TEXT_STARTER_REGEX = re.compile(TEXT_STARTER_PATTERN, flags=re.DOTALL)
PARATAGS_PATTERN = r'</?P>'
PARATAGS_REGEX = re.compile(PARATAGS_PATTERN)

def parse_from_new(filename):
    """Parse a novel document"""
    xml_string = ''
    text_starter_in = False
    with open(filename) as stream:
        for line in stream:
            line = XML_AMP_REGEX.sub(r'&amp;', line)
            line = XML_ATT_REGEX.sub(r'\1="\2"', line)
            line = PARATAGS_REGEX.sub('', line)
            xml_string += line
            if TEXT_STARTER in line:
                text_starter_in = True
    if text_starter_in:
        xml_string = TEXT_STARTER_REGEX.sub(r'\1\n\3', xml_string)
    root = ET.fromstring(xml_string)
    title = find_title(root)
    if title is DO_NOT_INCLUDE:
        return DO_NOT_INCLUDE
    doc_body = root.find('TEXT').text
    if doc_body == '' or doc_body == '\n':
        doc_body = root.find('LP').text
    doc_body = clean_input(doc_body)
    return {'title':title, 'doc_body': doc_body}

def read_from_training(filename):
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

def find_title(root): #pylint: disable = R0912
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
        title_node = root.find('HEADLINE')
        if title_node is not None:
            title = title_node.text
        else:
            title_node = root.find('HEAD')
            if title_node is not None:
                title = title_node.text
    if title == '':
        title_node = root.find('HL')
        if title_node is not None:
            title = title_node.text
        else:
            return DO_NOT_INCLUDE
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
    TEST_TEXT = '..\\test_docs\\d45h\\WSJ910628-0109'
    #'..\\duc01_tagged_meo_data\\d36f\\AP890322-0078.S'
    #'..\\duc01_tagged_meo_data\\d01a\\SJMN91-06184003.S'
    PARSED = parse_from_new(TEST_TEXT)
    print('title = ', PARSED['title'])
    print('doc_body = ', PARSED['doc_body'])
    #PARSED_SENTENCES = PARSED['sentences']
    #for list_entry in PARSED_SENTENCES:
    #    print('sentence text = ', list_entry['sentence'])
    #    print('sentence in summary? ', list_entry['in_summary'])
