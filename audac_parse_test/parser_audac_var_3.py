import requests_cache
from bs4 import BeautifulSoup
from pathlib import Path

import csv
import datetime as dt
from pprint import pprint
import pandas as pd

from openpyxl import Workbook

BASE_DIR = Path(__file__).parent
DATETIME_FORMAT = '%Y-%m-%d_%H-%M-%S'

MAIN_DOC_URL = 'https://audac.eu/eu/products/d/ateo4---wall-speaker-with-clevermount-4inch#section-specifications'

cnt = 0


if __name__ == '__main__':
    # Загрузка веб-страницы с кешированием.
    session = requests_cache.CachedSession()
    response = session.get(MAIN_DOC_URL)
    response.encoding = 'utf-8'
    results = []
    # results_1 = []
    # results_2 = []
    # results_3 = []

    # Создание "супа".
    soup = BeautifulSoup(response.text, features='lxml')

    # таблицу взяли
    all_spec_table = soup.find_all('table', attrs={'class': 'table table-hover mb-6 specification-table'})
    # print(all_spec_table)
    # tr_tags = system_spec_table.find_all('tr')


    # взял вторую таблицу из трех на странице. остальные потом/
    system_spec_table = all_spec_table[1]

    # product_features_table = all_spec_table[2]
    # print(system_spec_table)
    # print(product_features_table)


    soup_2 = BeautifulSoup(system_spec_table.text, features='lxml')

    tr_tags_spec = system_spec_table.find_all('tr')

    # # Проходим tr тэгам
    # for tr_tag_spec in tr_tags_spec:
    #     # print('!!!!!!!!!!!!!!!!!!!!!!!!!!')  # просто разделил чтоб подумать)
    #     print(tr_tag_spec)

    # print(tr_tags_spec)


    # table = []
    # for tr_tag in tr_tags_spec:
    #     row = []
    #     for td_tag in tr_tag.find_all('td'):
    #         colspan = td_tag.attrs.get('colspan', 1)
    #         row.append(td_tag.text or None)
    #         row += [None] * (int(colspan) - 1)
    #     table.append(row)

    # pprint(table)

    table = []
    for tr_tag in tr_tags_spec:
        row = []
        for td_tag in tr_tag.find_all('td'):
            colspan = td_tag.attrs.get('colspan')
            row.append(td_tag.text or None)
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
            row = [row[0], '|', None, '||']
            upd_row = [' ' * 10 + c1, '|', c2, '||']
            upd_table.append(row)
            upd_table.append(upd_row)

    pprint(upd_table)



    # рабочий
    results_dir = BASE_DIR / 'results'
    results_dir.mkdir(exist_ok=True)

    now = dt.datetime.now()
    now_formatted = now.strftime(DATETIME_FORMAT)
    # file_name = f'{now_formatted}.csv'
    file_name = f'{now_formatted}.xlsx'
    file_path = results_dir / file_name
    df = pd.DataFrame(upd_table)
    # df = pd.DataFrame(table)
    df.to_excel('file_path.xlsx', index=0, header=False)


    # results_dir = BASE_DIR / 'results'
    # results_dir.mkdir(exist_ok=True)

    # now = dt.datetime.now()
    # now_formatted = now.strftime(DATETIME_FORMAT)
    # file_name = f'{now_formatted}.csv'
    # file_path = results_dir / file_name
    # with open(file_path, 'w', encoding='utf-8') as f:
    #     writer = csv.writer(f, delimiter=',')
    #     # for i in results:
    #     writer.writerows(upd_table)
