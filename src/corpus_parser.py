"""Read in original texts and reference summaries from corpus"""
import xml.etree.ElementTree as ET
import re
PUNCTUATION_PATTERN = r'(,|\'|\"|;|&|-|:|\$)'
PUNCTUATION_REGEX = re.compile(PUNCTUATION_PATTERN)
BRACKETED_KEYWORDS_PATTERN = r'\([A-Z]*\)'
BRACKETED_KEYWORDS_REGEX = re.compile(BRACKETED_KEYWORDS_PATTERN)
BRACKETS_PATTERN = r'[\(\)]'
BRACKETS_REGEX = re.compile(BRACKETS_PATTERN)

def parse_original_text(filename, style='wsj'):
    """Read in original text"""
    xml_string = ''
    with open(filename) as stream:
        for line in stream:
            line = re.sub(r'[\[\]]', '\"', line)
            line = re.sub(r'&(?!amp;)', r'&amp;', line)
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
    #Might just use wsj texts as they have keywords
    return {'text': clean_input(text, 'body'),
            'title': clean_input(title, 'title'),
            'has_keywords': has_keywords,
            'keywords': clean_input(keywords, 'keywords')}

def parse_scored_text(filename, tag_type='categ'):
    """Parse a scored summary of a text from a file"""
    xml_string = '<DOC>'
    line_count = 0
    header_lines = []
    with open(filename) as stream:
        for line in stream:
            if line_count < 4:
                header_lines.append(line)
                line_count = line_count + 1
            else:
                line = re.sub(r'[\[\]]', '\"', line)
                line = re.sub(r'&(?!amp;)', r'&amp;', line)
                xml_string = xml_string + line
    xml_string = xml_string + '</DOC>'
    #try:
    root = ET.fromstring(xml_string)
    #except Exception as exp:
    #    print('Error reading file', filename)
    #    raise exp.with_traceback("Error reading file filename")
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

    for sentence in sentences:
        sentence['best_score'] = sentence['best_score'] / max_best_score
        sentence['fixed_score'] = sentence['fixed_score'] / max_fixed_score
    return sentences

def clean_input(text, section='body'):
    """Remove unnecessary chars from input"""
    return_text = text
    if section == 'title':
        text = re.split(r'\s----\s', text)
        return_text = text[0]
    return_text = PUNCTUATION_REGEX.sub(' ', return_text)
    if section == 'keywords':
        return_text = BRACKETED_KEYWORDS_REGEX.sub('', return_text)
    else:
        return_text = BRACKETS_REGEX.sub(' ', return_text)
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
