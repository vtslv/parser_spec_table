# import os
import datetime as dt

from pathlib import Path

import pandas as pd
from pandas.io.excel import ExcelWriter

import logging

BASE_DIR = Path(__file__).parent
DATETIME_FORMAT = '%Y-%m-%d_%H-%M-%S'

def output(upd_table):

    # xlsx_path = BASE_DIR + r'\result.xlsx'
    results_dir = BASE_DIR / 'results'
    results_dir.mkdir(exist_ok=True)

    now = dt.datetime.now()
    now_formatted = now.strftime(DATETIME_FORMAT)
    file_name = f'{now_formatted}.xlsx'
    file_path = results_dir / file_name


    df = pd.DataFrame(upd_table)

    with ExcelWriter(file_path) as writer:
        df.to_excel(writer, index=0, header=False, sheet_name='test')

    logging.info(f'Файл с результатами был сохранён: {file_path}')
