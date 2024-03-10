import logging
from pathlib import Path

import pandas as pd
from pandas.io.excel import ExcelWriter

BASE_DIR = Path(__file__).parent


def output(upd_table, page_name):
    logging.info('Запись в Excel...')
    results_dir = BASE_DIR / 'results'
    results_dir.mkdir(exist_ok=True)
    file_name = 'audac_parser_result.xlsx'
    file_path = results_dir / file_name
    df = pd.DataFrame(upd_table)
    sheet_name = page_name
    if file_path.exists():
        with ExcelWriter(
            file_path,
            mode='a',
            if_sheet_exists='replace'
        ) as writer:
            df.to_excel(
                writer,
                index=0,
                header=False,
                sheet_name=sheet_name
            )
        logging.info(f'Файл с результатами был ПЕРЕЗАПИСАН: {file_path}')

    else:
        with ExcelWriter(
            file_path,
            mode='w',
        ) as writer:
            df.to_excel(
                writer,
                index=0,
                header=False,
                sheet_name=sheet_name
            )
        logging.info(f'Файл с результатами был СОХРАНЕН: {file_path}')
