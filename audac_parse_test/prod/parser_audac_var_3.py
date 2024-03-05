# import requests_cache
# from bs4 import BeautifulSoup
# from pathlib import Path

# import csv
# import datetime as dt
# from pprint import pprint
# import pandas as pd

# from openpyxl import Workbook

# BASE_DIR = Path(__file__).parent
# DATETIME_FORMAT = '%Y-%m-%d_%H-%M-%S'

# MAIN_DOC_URL = 'https://audac.eu/eu/products/d/ateo4---wall-speaker-with-clevermount-4inch#section-specifications'

# cnt = 0


# if __name__ == '__main__':
#     # Загрузка веб-страницы с кешированием.
#     session = requests_cache.CachedSession()
#     response = session.get(MAIN_DOC_URL)
#     response.encoding = 'utf-8'


#     # Создание "супа".
#     soup = BeautifulSoup(response.text, features='lxml')

#     # таблицу взяли
#     all_spec_table = soup.find_all(
#         'table',
#         attrs={'class': 'table table-hover mb-6 specification-table'}
#     )


#     tables_lst = []



#     # взял вторую таблицу из трех на странице. остальные потом/
#     system_spec_table = all_spec_table[1]

#     # product_features_table = all_spec_table[2]

#     soup_2 = BeautifulSoup(system_spec_table.text, features='lxml')

#     tr_tags_spec = system_spec_table.find_all('tr')

#     table = []
#     for tr_tag in tr_tags_spec:
#         row = []
#         for td_tag in tr_tag.find_all('td'):
#             colspan = td_tag.attrs.get('colspan')
#             # row.append(td_tag.text or None)
#             row.append(td_tag.text or '-')
#         table.append(row)

#     # pprint(table)

#     upd_table = [['Характеристика', '|', 'Значение', '||']]

#     for row in table:
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

#     pprint(upd_table)




#     # рабочий
#     results_dir = BASE_DIR / 'results'
#     results_dir.mkdir(exist_ok=True)

#     now = dt.datetime.now()
#     now_formatted = now.strftime(DATETIME_FORMAT)
#     # file_name = f'{now_formatted}.csv'
#     file_name = f'{now_formatted}.xlsx'
#     file_path = results_dir / file_name
#     df = pd.DataFrame(upd_table)
#     # df = pd.DataFrame(table)
#     df.to_excel('file_path.xlsx', index=0, header=False)









import csv
import datetime as dt
import os
from pathlib import Path
from pprint import pprint

import pandas as pd
import requests_cache
from bs4 import BeautifulSoup
from openpyxl import Workbook
from pandas.io.excel import ExcelWriter

BASE_DIR = Path(__file__).parent
DATETIME_FORMAT = '%Y-%m-%d_%H-%M-%S'

PRODUCTS_URL = [
    'https://audac.eu/eu/products/d/ateo4---wall-speaker-with-clevermount-4inch#section-specifications']
#     'https://audac.eu/eu/products/d/alti6---2-way-6inch-pendant-speaker#section-specifications',
#     'https://audac.eu/eu/products/d/xeno6---full-range-speaker-6inch#section-specifications'
# ]


def get_spec_tables_lst():
    # Загрузка веб-страницы с кешированием.
    specs_table_lst = []
    session = requests_cache.CachedSession()
    for product_url in PRODUCTS_URL:
        response = session.get(product_url)
        response.encoding = 'utf-8'

        # Создание "супа".
        url_soup = BeautifulSoup(response.text, features='lxml')

        # таблицу взяли
        all_spec_table_lst = url_soup.find_all(
            'table',
            attrs={'class': 'table table-hover mb-6 specification-table'}
        )

        # взял вторую таблицу из трех на странице. остальные потом/


        specs_table_lst.append(all_spec_table_lst[1])
        # specs_table_lst.append(all_spec_table_lst[2])
        # print(specs_table_lst)

        for spec_table in specs_table_lst:
            tr_lst = []
            spec_table_soup = BeautifulSoup(spec_table.text, features='lxml')
            tr_tags_spec = spec_table.find_all('tr')
            print(spec_table_soup)
            return tr_tags_spec
            # tr_lst.append(tr_tags_spec)
            # pprint(tr_lst)

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
    return output(upd_table)
    # pprint(upd_table)


def output(upd_table):

    xlsx_path = os.path.dirname(__file__) + r'\result.xlsx'
    df = pd.DataFrame(upd_table)
    with ExcelWriter(xlsx_path) as writer:
        df.to_excel(writer, index=0, header=False, sheet_name='test')


def main():
    a = get_spec_tables_lst()
    aaa(a)

if __name__ == '__main__':

    main()
