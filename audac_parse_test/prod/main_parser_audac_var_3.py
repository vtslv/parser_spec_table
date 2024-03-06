import logging
from pathlib import Path

# import pandas as pd
import requests_cache
from bs4 import BeautifulSoup
from configs import configure_logging
# from openpyxl import Workbook
from output import output
# from pandas.io.excel import ExcelWriter
from utils import get_response

# import datetime as dt
# from pprint import pprint


BASE_DIR = Path(__file__).parent
DATETIME_FORMAT = '%Y-%m-%d_%H-%M-%S'

PRODUCTS_URL = 'https://audac.eu/eu/products/d/ateo4---wall-speaker-with-clevermount-4inch#section-specifications'

# PRODUCTS_URL = [
#    'https://audac.eu/eu/products/d/ateo4---wall-speaker-with-clevermount-4inch#section-specifications']
#     'https://audac.eu/eu/products/d/alti6---2-way-6inch-pendant-speaker#section-specifications',
#     'https://audac.eu/eu/products/d/xeno6---full-range-speaker-6inch#section-specifications'
# ]


def get_spec_tables_lst():
    # Загрузка веб-страницы с кешированием.
    session = requests_cache.CachedSession()
    # for product_url in PRODUCTS_URL:
    #     response = session.get(product_url)

    # response = session.get(PRODUCTS_URL)
    # response.encoding = 'utf-8'

    response = get_response(session, PRODUCTS_URL)
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
            row.append(td_tag.text or '-')
        td_tag_text_table.append(row)
    logging.info('Получен текст "td" тэгов!')
    return td_tag_text_table


def formation_text_table(td_table):
    upd_table = [['Характеристика', '|', 'Значение', '||']]
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
        d = ['-', '|', '-', '||']
        if row == d:
            upd_table.pop(i)
    logging.info('Таблица готова к записи!')
    return upd_table


def main():
    configure_logging()
    logging.info('Парсер запущен!')
    td_table = get_spec_tables_lst()
    results = formation_text_table(td_table)
    if results is not None:
        output(results)
    logging.info('Парсер завершил работу.')


if __name__ == '__main__':
    main()
