import datetime as dt
import logging
# import os
from pathlib import Path
from urllib.parse import urlparse

import pandas as pd
from pandas.io.excel import ExcelWriter

BASE_DIR = Path(__file__).parent
DATETIME_FORMAT = '%Y-%m-%d_%H-%M-%S'


def output(upd_table, page_name):
    logging.info('Запись в Excel...')
    # xlsx_path = BASE_DIR + r'\result.xlsx'
    results_dir = BASE_DIR / 'results'
    results_dir.mkdir(exist_ok=True)
    now = dt.datetime.now()
    now_formatted = now.strftime(DATETIME_FORMAT)
    file_name = f'{now_formatted}.xlsx'
    file_path = results_dir / file_name
    df = pd.DataFrame(upd_table)
    with ExcelWriter(file_path) as writer:
        df.to_excel(writer, index=0, header=False, sheet_name=page_name)
    logging.info(f'Файл с результатами был сохранён: {file_path}')


# def output(upd_table):
#     xlsx_path = os.path.dirname(__file__) + r'\result.xlsx'
#     df = pd.DataFrame(upd_table)
#     with ExcelWriter(xlsx_path) as writer:
#         df.to_excel(writer, index=0, header=False, sheet_name='test')

# вот то доделать!!!!!!!!!!!!!!!!!!!!!

# def output(upd_table):
#     logging.info('Запись в Excel...')
#     results_dir = BASE_DIR / 'results'
#     results_dir.mkdir(exist_ok=True)
#     file_name = f'audac_parser_result.xlsx'
#     file_path = results_dir / file_name
#     df = pd.DataFrame(upd_table)
#     sheet_name = 'Лист_1'
#     with ExcelWriter(
#         file_name,
#         mode='a' if BASE_DIR.exists() else 'w'
#     ) as writer:
#         df.to_excel(
#             writer,
#             index=0,
#             header=False,
#             sheet_name=sheet_name
#         )
#     logging.info(f'Файл с результатами был сохранён: {file_path}')


#     f_url = 'https://audac.eu/eu/products/d/ateo4---wall-speaker-with-clevermount-4inch#section-specifications'
#     o = urlparse(f_url)
#     a = o.path
#     # print(a)

#     # /eu/products/d/ateo4-
#     b = a.split('/')[4]
#     f = b.split('-')[0]
#     print(f)
