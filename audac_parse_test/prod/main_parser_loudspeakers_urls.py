# import csv
import logging
from pathlib import Path
from pprint import pprint
from urllib.parse import urljoin, urlparse

# import pandas as pd
import requests_cache
from bs4 import BeautifulSoup
from configs import configure_logging
from constants import PRODUCT_URLS
from keyword_replace import replace_td_tag_text_ru
from output import output
from unique_lines import uniquelines
from utils import find_tag, get_response

BASE_DIR = Path(__file__).parent
MAIN_URL = 'https://audac.eu'
LOUDSPEAKERS_URL = 'https://audac.eu/eu/#1083-loudspeakers'


# def get_page_name(url):
#     # url_path = urlparse(PRODUCTS_URL).path
#     url_path = urlparse(url).path
#     # url_path = url
#     # /eu/products/d/ateo4-
#     url_path_right = url_path.split('/')[4]
#     page_name = url_path_right.split('-')[0].upper()
#     return page_name


# def get_spec_tables_lst(url):
#     # Загрузка веб-страницы с кешированием.
#     session = requests_cache.CachedSession()
#     response = get_response(session, url)
#     if response is None:
#         return
#     # Создание "супа".
#     url_soup = BeautifulSoup(response.text, features='lxml')
#     # таблицу взяли
#     all_spec_table_bs = url_soup.find_all(
#         'table',
#         attrs={'class': 'table table-hover mb-6 specification-table'}
#     )
#     # взял вторую таблицу из трех на странице. остальные потом/
#     first_spec_table_bs = all_spec_table_bs[1]
#     second_spec_table_bs = all_spec_table_bs[2]
#     first_spec_table_bs.append(second_spec_table_bs)
#     tr_tags_spec = first_spec_table_bs.find_all('tr')
#     logging.info('Получены все "tr" тэги!')
#     td_tag_text_table = []
#     logging.info('Получение текста "td" тэгов...')
#     for tr_tag in tr_tags_spec:
#         row = []
#         for td_tag in tr_tag.find_all('td'):
#             # row.append(td_tag.text or '-')
#             td_text = td_tag.text
#             td_tag_text_ru = replace_td_tag_text_ru(td_text)
#             row.append(td_tag_text_ru or '-')
#             # вспомогательный файл temp для значений для перевода.
#             txt_file_name = 'temp_file_for_replace.txt'
#             with open(txt_file_name, 'a', encoding='utf-8') as output:
#                 output.write(td_text + '\n')
#         td_tag_text_table.append(row)
#     logging.info('Получен текст "td" тэгов!')
#     return td_tag_text_table


# def formation_text_table(td_table):
#     # upd_table = [['Характеристика', '|', 'Значение', '||']]
#     upd_table = []
#     logging.info('Форматирование таблицы...')
#     for row in td_table:
#         if len(row) == 2:
#             row.insert(1, '|')
#             row.insert(3, '||')
#             upd_table.append(row)

#         elif len(row) > 2:
#             c1 = row[1]
#             c2 = row[2]
#             # row = [row[0], '|', None, '||']
#             row = [row[0], '|', '-', '||']
#             upd_table.append(row)
#             upd_row = [' ' * 10 + c1, '|', c2, '||']
#             upd_table.append(upd_row)
#     logging.info('Форматирование таблицы звавершено!')
#     return empty_row_delete(upd_table)


# def empty_row_delete(upd_table):
#     logging.info('Удаление пустых строк...')
#     for i, row in enumerate(upd_table):
#         # ['-', '|', '-', '||']
#         if row == ['-', '|', '-', '||']:
#             upd_table.pop(i)
#     logging.info('Таблица готова к записи!')
#     return upd_table


def main():
    configure_logging()
    logging.info('Парсер запущен!')
    # очищаем вспомогательный файл temp
    # f = open('temp_file_for_replace.txt', 'w+', encoding='utf-8')
    # f.close()
    loudspeaker_url_list = parse_url_speakers_series(LOUDSPEAKERS_URL)
    # pprint(loudspeaker_url_list)
    # for ls_series_link in loudspeaker_url_list:
    #     # список ссылок на продукты в серии (эти ссылки нужно аппендить в общий список)
    #     product_by_series_url_list = parse_by_series(ls_series_link)
    # pprint(loudspeaker_url_list)
    # for k_name, v_link in loudspeaker_url_list.items():
    product_by_series_url_list = parse_by_series(loudspeaker_url_list)


    # for url in PRODUCT_URLS:
    #     page_name = get_page_name(url)
    #     td_table = get_spec_tables_lst(url)
    #     results = formation_text_table(td_table)
    #     if results is not None:
    #         output(results, page_name)
    logging.info('Создание уникальных значений для перевода...')
    # uniquelines()
    logging.info('Парсер завершил работу.')









def parse_url_speakers_series(url):
    """Парсер урлов на серии АС."""
    session = requests_cache.CachedSession()
    response = get_response(session, url)
    if response is None:
        return
    soup = BeautifulSoup(response.text, features='lxml')
    sidebar = find_tag(soup, 'div', attrs={'id': '1083-loudspeakers'})

    a_tags = sidebar.find_all('a')
    ls_series_links_lst = []
    dict_sample = {}
    for a_tag in a_tags:
        ls_series_links = a_tag['href']
        link_txt = a_tag.text
        short_link_text = link_txt.split()
        ls_series_links_lst.append(ls_series_links)
        dict_sample[short_link_text[0]] = ls_series_links
    # pprint(dict_sample)


    # return ls_series_links_lst
    return dict_sample


# def parse_by_series(ls_series_link):
def parse_by_series(loudspeaker_url_list):
    """Парсер о нововведениях в Python."""
    session = requests_cache.CachedSession()
    var1 = ['ATEO', 'ALTI', 'VEXO', 'CENA', 'BASO', 'HS']
    var2 = ['NOBA', 'VIRO', 'NOBA/A']
    var3 = ['WX/O', 'XENO', 'FX', 'CELO', 'MERO', 'CALI', 'CIRA', 'VEXO/A', 'KYRA', 'LINO', 'CHA', 'SP', 'WX']

    for k_name, v_link in loudspeaker_url_list.items():
        if k_name in var1:
            by_series_url = urljoin(MAIN_URL, v_link)
            response = get_response(session, by_series_url)
            if response is None:
                return
            soup = BeautifulSoup(response.text, features='lxml')
            product_splide = find_tag(soup, 'div', attrs={'class': 'splide__track'})
            li_tags = find_tag(product_splide, 'a', attrs={'class': 'product comparison h-100'})
            # for li in li_tags:
            # a_tag = find_tag(li_tags, 'a')
            # link_href = a_tag['href']
            # !!!!!!!!!!!!!!!!!!!!!!хз как тут найти ссылки
            pprint(li_tags)

        elif k_name in var2:
            by_series_url = urljoin(MAIN_URL, v_link)
            pass
        elif k_name in var3:
            by_series_url = urljoin(MAIN_URL, v_link)
            pass

    # by_series_url = urljoin(MAIN_URL, ls_series_link)
    # response = get_response(session, by_series_url)
    # if response is None:
    #     return
    # soup = BeautifulSoup(response.text, features='lxml')
    # # product_splide = find_tag(soup, 'ul', attrs={'class': 'splide__list'})
    # product_splide = find_tag(soup, 'div', attrs={
    #     'class': 'splide__track splide__track--slide splide__track--ltr splide__track--draggable',
    #     'class': 'col-sm-6 col-md-4 col-lg-3 pb-3'})


    # a_tags = product_splide.find_all('a')
    # pprint(a_tags)


    li_tags = product_splide.find_all('li')
    # for li in li_tags:
    #     a_tags = li.find_all('a')

    # pprint(a_tags)

    # a_tags = product_splide.find_all('a')
    # product_series_links_lst = []
    # for a_tag in a_tags:
    #     product_series_links = a_tag['href']
    #     link_txt = a_tag.text
    #     product_series_links_lst.append(product_series_links)

        # pprint(a_tags)


    # for ul in ul_tags:
    #     if 'All versions' in ul.text:
    #         a_tags = ul.find_all('a')
    #         break
    # else:
    #     raise Exception('Ничего не нашлось')
    # results = [('Ссылка на документацию', 'Версия', 'Статус')]
    # pattern = r'Python (?P<version>\d\.\d+) \((?P<status>.*)\)'
    # for a_tag in a_tags:
    #     link = a_tag['href']
    #     text_match = re.search(pattern, a_tag.text)
    #     if text_match is not None:
    #         version, status = text_match.groups()
    #     else:
    #         version, status = a_tag.text, ''
    #     results.append(
    #         (link, version, status)
    #     )
    # return results


if __name__ == '__main__':
    main()
