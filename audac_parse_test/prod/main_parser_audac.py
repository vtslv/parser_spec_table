# import csv
import logging
from pathlib import Path
# from pprint import pprint
from urllib.parse import urlparse

# import pandas as pd
import requests_cache
from bs4 import BeautifulSoup
from configs import configure_logging
from constants import PRODUCT_URLS
from keyword_replace import replace_td_tag_text_ru
from output import output
from unique_lines import uniquelines
from utils import get_response

BASE_DIR = Path(__file__).parent


def get_page_name(url):
    # url_path = urlparse(PRODUCTS_URL).path
    url_path = urlparse(url).path
    # url_path = url
    # /eu/products/d/ateo4-
    url_path_right = url_path.split('/')[4]
    page_name = url_path_right.split('-')[0].upper()
    return page_name


def get_spec_tables_lst(url):
    # Загрузка веб-страницы с кешированием.
    session = requests_cache.CachedSession()
    response = get_response(session, url)
    if response is None:
        return
    # Создание "супа".
    url_soup = BeautifulSoup(response.text, features='lxml')
    # таблицу взяли
    all_spec_table_bs = url_soup.find_all(
        'table',
        attrs={'class': 'table table-hover mb-6 specification-table'}
    )
    # взял вторую таблицу из трех на странице. остальные потом/
    first_spec_table_bs = all_spec_table_bs[1]
    second_spec_table_bs = all_spec_table_bs[2]
    first_spec_table_bs.append(second_spec_table_bs)
    tr_tags_spec = first_spec_table_bs.find_all('tr')
    logging.info('Получены все "tr" тэги!')
    td_tag_text_table = []
    logging.info('Получение текста "td" тэгов...')
    for tr_tag in tr_tags_spec:
        row = []
        for td_tag in tr_tag.find_all('td'):
            # row.append(td_tag.text or '-')
            td_text = td_tag.text
            td_tag_text_ru = replace_td_tag_text_ru(td_text)
            row.append(td_tag_text_ru or '-')
            # вспомогательный файл temp для значений для перевода.
            txt_file_name = 'temp_file_for_replace.txt'
            with open(txt_file_name, 'a', encoding='utf-8') as output:
                output.write(td_text + '\n')
        td_tag_text_table.append(row)
    logging.info('Получен текст "td" тэгов!')
    return td_tag_text_table


def formation_text_table(td_table):
    # upd_table = [['Характеристика', '|', 'Значение', '||']]
    upd_table = []
    logging.info('Форматирование таблицы...')
    for row in td_table:
        if len(row) == 2:
            row.insert(1, '|')
            row.insert(3, '||')
            upd_table.append(row)

        elif len(row) > 2:
            c1 = row[1]
            c2 = row[2]
            # row = [row[0], '|', None, '||']
            row = [row[0], '|', '-', '||']
            upd_table.append(row)
            upd_row = [' ' * 10 + c1, '|', c2, '||']
            upd_table.append(upd_row)
    logging.info('Форматирование таблицы звавершено!')
    return empty_row_delete(upd_table)


def empty_row_delete(upd_table):
    logging.info('Удаление пустых строк...')
    for i, row in enumerate(upd_table):
        # ['-', '|', '-', '||']
        if row == ['-', '|', '-', '||']:
            upd_table.pop(i)
    logging.info('Таблица готова к записи!')
    return upd_table


def main():
    configure_logging()
    logging.info('Парсер запущен!')
    # очищаем вспомогательный файл temp
    f = open('temp_file_for_replace.txt', 'w+', encoding='utf-8')
    f.close()
    for url in PRODUCT_URLS:
        page_name = get_page_name(url)
        td_table = get_spec_tables_lst(url)
        results = formation_text_table(td_table)
        if results is not None:
            output(results, page_name)
    logging.info('Создание уникальных значений для перевода...')
    uniquelines()
    logging.info('Парсер завершил работу.')


# есть проблема с урлами в урлпарс.паф
# def main():
#     configure_logging()
#     logging.info('Парсер запущен!')
#     # for url in PRODUCT_URLS:
#     csv_dir = BASE_DIR / 'import_urls'
#     csv_file_name = f'urls.csv'
#     file_path = csv_dir / csv_file_name

#     with open(
#         file_path,
#         'r',
#         # encoding='utf-8',
#     ) as csv_url_file:
#         csvreader = csv.reader(csv_url_file)
#         for url in csvreader:
#             page_name = get_page_name(url)
#             td_table = get_spec_tables_lst(url)
#             results = formation_text_table(td_table)
#             if results is not None:
#                 output(results, page_name)
#     logging.info('Парсер завершил работу.')


if __name__ == '__main__':
    main()
