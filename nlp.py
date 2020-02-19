import re

from functions import text_cleaner
from spacy.matcher import Matcher
from spacy.matcher import PhraseMatcher

def parse_money(text):

    money_amt = 0
    format_money = re.compile('(\d{1,3}(?:.\d{3})*(?:\.\d+))')

    for m in format_money.finditer(text):
        if text[m.start()-2:m.end()][0] == "$":
            money_str = text[m.start():m.end()]
            money_amt += float(money_str.replace(".", '').replace(",", '').replace(' ', ''))

    return money_amt


def parse_business(nlp_spacy, text):

    matcher = Matcher(nlp_spacy.vocab)

    pattern1 = [{'LOWER': 'sa'}]
    pattern2 = [{'LOWER': 'sas'}]
    pattern3 = [{'LOWER': 'srl'}]
    pattern4 = [{'LOWER': 'saas'}]

    matcher.add('business_names', None, pattern1, pattern2, pattern3, pattern4)

    custom_stopword = ['firma', 'adjudicado', 'proveedor', 'razón', 'social',
                        'adjudicada', 'oferente', 'adjudicatario', 'adjudicar',
                        'empresa', 'contratación', 'aceptado', 'adjudicación',
                        'fracasado', 'firmas']

    token_offset=3

    text = nlp_spacy(text_cleaner(text.lower()))
    found_matches = matcher(text)

    business_list = []

    for match_id, start, end in found_matches:
        span = text[(start - token_offset):end]
        business_list.append(text_cleaner(span.text, custom_stopword))

    return list(dict.fromkeys(business_list))
