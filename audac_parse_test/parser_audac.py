import requests_cache
from bs4 import BeautifulSoup
from pathlib import Path

import csv
import datetime as dt

BASE_DIR = Path(__file__).parent
DATETIME_FORMAT = '%Y-%m-%d_%H-%M-%S'

MAIN_DOC_URL = 'https://audac.eu/eu/products/d/ateo4---wall-speaker-with-clevermount-4inch#section-specifications'


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


    system_spec_table = all_spec_table[1]
    product_features_table = all_spec_table[2]
    # print(product_features_table)

    soup_2 = BeautifulSoup(system_spec_table.text, features='lxml')

    tr_tags_spec = system_spec_table.find_all('tr')
    for tr_tag_spec in tr_tags_spec:

        # tr_tag_column =
        # print(tr_tag_spec.text)
        # results.append((tr_tag.text))

        # td_tag_spec = tr_tag_spec.find('td')
        # td_tag_colspan = tr_tag_spec.find_all('td colspan="2"')
        # td_tag_colspan = td_tag_spec.find_next()


        # print(td_tag_spec.text)
        # print(td_tag_colspan)

        # = dt_tag.find_next_sibling().string

        # results_1.append(td_tag_spec.text)
        # print(results)
        results.append(tr_tag_spec.text)







    results_dir = BASE_DIR / 'results'
    results_dir.mkdir(exist_ok=True)

    now = dt.datetime.now()
    now_formatted = now.strftime(DATETIME_FORMAT)
    file_name = f'{now_formatted}.csv'
    file_path = results_dir / file_name
    with open(file_path, 'w', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=' ')
        # for i in results:
        writer.writerow(results)
            # writer.writerow([i])


    print(results)

    # print(results_1)
    # print(results_2)
    # print(results_3)


