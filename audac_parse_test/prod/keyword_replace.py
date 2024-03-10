from constants import keyword_dictionary
from flashtext import KeywordProcessor


def replace_td_tag_text_ru(td_text):
    '''Замена англ текста td тэгов на русский'''
    keyword_processor = KeywordProcessor()
    keyword_processor.add_keywords_from_dict(keyword_dictionary)
    return keyword_processor.replace_keywords(td_text)
