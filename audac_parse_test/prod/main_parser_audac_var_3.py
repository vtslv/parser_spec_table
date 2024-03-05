import logging
from pathlib import Path

# import datetime as dt
# from pprint import pprint
# import pandas as pd
import requests_cache
from bs4 import BeautifulSoup
from configs import configure_logging
# from openpyxl import Workbook
from output import output
# from pandas.io.excel import ExcelWriter
from utils import get_response

# import pandas as pd
# import os


BASE_DIR = Path(__file__).parent
DATETIME_FORMAT = '%Y-%m-%d_%H-%M-%S'

PRODUCTS_URL = 'https://audac.eu/eu/products/d/ateo4---wall-speaker-with-clevermount-4inch#section-specifications'

# PRODUCTS_URL = [
#    'https://audac.eu/eu/products/d/ateo4---wall-speaker-with-clevermount-4inch#section-specifications']
#     'https://audac.eu/eu/products/d/alti6---2-way-6inch-pendant-speaker#section-specifications',
#     'https://audac.eu/eu/products/d/xeno6---full-range-speaker-6inch#section-specifications'
# ]


# def get_response(session, url):
#     """Перехват ошибки RequestException."""
#     try:
#         response = session.get(url)
#         response.encoding = 'utf-8'
#         return response
#     except RequestException:
#         logging.exception(
#             f'Возникла ошибка при загрузке страницы {url}',
#             stack_info=True
#         )

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

    # spec_table_soup = BeautifulSoup(
    #     first_spec_table_bs.text,
    #     features='lxml'
    # )
    tr_tags_spec = first_spec_table_bs.find_all('tr')
    return tr_tags_spec


def aaa(tr_tags_spec):
    table = []
    for tr_tag in tr_tags_spec:
        row = []
        for td_tag in tr_tag.find_all('td'):
            # colspan = td_tag.attrs.get('colspan')
            # row.append(td_tag.text or None)
            row.append(td_tag.text or '-')
        table.append(row)

    # pprint(table)

    upd_table = [['Характеристика', '|', 'Значение', '||']]

    for row in table:
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
    # return output(upd_table)
    return upd_table
    # pprint(upd_table)


# def output(upd_table):

#     xlsx_path = os.path.dirname(__file__) + r'\result.xlsx'
#     df = pd.DataFrame(upd_table)
#     with ExcelWriter(xlsx_path) as writer:
#         df.to_excel(writer, index=0, header=False, sheet_name='test')


def main():
    configure_logging()
    logging.info('Парсер запущен!')

    a = get_spec_tables_lst()
    results = aaa(a)

    if results is not None:
        output(results)
    logging.info('Парсер завершил работу.')


if __name__ == '__main__':
    main()
