#!/usr/bin/env python
# coding: utf-8
from bs4 import BeautifulSoup
from datetime import timedelta
import requests
import requests
import requests_cache
from time import sleep

requests_cache.install_cache(
    'cache',
    expire_after=timedelta(hours=24),
    allowable_methods=('GET', 'POST')
)

SEARCH_URL = 'https://report.boonecountymo.org/mrcjava/servlet/RMS01_MP.I00030s?max_rows=10000'


# "Don't need to 'get_injury_types'"


# def get_search_results():
#     r = requests.get(
#         SEARCH_URL,
#         headers={'user-agent': "I'm good people!!!"}
#     )
#     soup = BeautifulSoup(r.content)
#
#     main_table = soup.find('tbody', id='mrc_main_table').find_all('tr')
#
#     detainees = []
#
#     for mtab in main_table:
#         td = mtab.attrs['class']
#         detainees.append(td)
#
#     return detainees

def get_search_results():
    r = requests.get(
        SEARCH_URL,
        headers={'user-agent': "I'm good people!!!"}
    )
    soup = BeautifulSoup(r.content)

    r.raise_for_status()

    return r.content


def extract_details_url(search_results):
    soup = BeautifulSoup(search_results)

    details_urls = []

    table = soup.find('table', class_='collapse data-table shadow responsive')

    tr_all = table.find_all('tr', class_=['odd', 'even'])

    for tr in tr_all:
        td_all = tr.find_all('td')
        url = td_all[9].find('a').attrs['href']
        details_urls.append(url)

    return details_urls


def main():
    search_results = get_search_results()
    urls = extract_details_url(search_results)
    print(urls)
    print('-----------------------')
    sleep(3)


if __name__ == '__main__':
    main()



# url = 'https://report.boonecountymo.org/mrcjava/servlet/RMS01_MP.I00030s'
#
#
# r = requests.get(
#     "https://report.boonecountymo.org/mrcjava/servlet/RMS01_MP.I00030s",
#     params={"max_rows": 10000},
#     headers={'user-agent': "I'm good people!!!"}
# )
#
#
# type(r)
#
#
# r.ok
#
#
# r.status_code
#
#
# r.reason
#
#
# dir(r)
#
#
# r.content
#
#
# post_r = requests.post(url, params={'rls_lastname': 'C0'})
#
#
# post_r.ok
#
#
# type(r.content)
#
#
# type(r.text)
#
#
# r.text
#
#
# with open ('search-results.html', 'w') as f:
#     f.write(r.text)
#
#
# from bs4 import BeautifulSoup
#
#
# soup = BeautifulSoup(r.text)
#
#
# type(soup)
#
#
# table = soup.find('table', class_= 'collapse data-table shadow responsive')
#
#
# type(table)
#
#
# table
#
#
# table.find_all('th')
#
#
# th_all = table.find('thead').find_all('tr')[1].find_all('th')
#
#
# th_all
#
#
# type(th_all)
#
#
# for th in th_all:
#     print(th.text)
#
#
# headers = []
#
#
# for th in th_all:
#     header = th.text.strip().replace(' ', '_').lower()
#     headers.append(header)
#
#
# headers
#
#
# tr_all = table.find_all('tr')[2:183]
#
#
# for tr in tr_all:
#     for td in tr.find_all('td'):
#         print(td.text.strip())
#     print('---------------')
#
#
# def clean_row(tds):
#     return tds
#
#
# for tr in tr_all:
#     print('--------------')
#     tds = tr.find_all('td')
#     row = clean_row(tds)
#     print(row)
#
#
# def clean_row(tds):
#     row = {
#         'details_url': tds[9].find('a').attrs['href'],
#         'last_name': tds[0].text.strip(),
#         'first_name': tds[1].text.strip(),
#         'middle_name': tds[2].text.strip(),
#         'suffix': tds[3].text.strip(),
#         'sex': tds[4].text.strip(),
#         'race': tds[5].text.strip(),
#         'age': int(tds[6].text.strip()),
#         'city': tds[7].text.strip(),
#         'state': tds[8].text.strip()
#     }
#     return row
#
#
# rows = []
#
#
# for tr in tr_all:
#     tds = tr.find_all('td')
#     row = clean_row(tds)
#     rows.append(row)
#
#
# rows
#
#
# import csv
#
#
# rows[0].keys()
#
#
# with open('jail.csv', 'w', newline='') as f:
#     writer = csv.DictWriter(
#         f, fieldnames=rows[0].keys()
#     )
#
#     writer.writeheader()
#     for row in rows:
#         writer.writerow(row)
