#!/usr/bin/env python
# coding: utf-8
from bs4 import BeautifulSoup
from datetime import timedelta
import requests
import requests
import requests_cache
from time import sleep
from models import Info, Charges

requests_cache.install_cache(
    'cache',
    expire_after=timedelta(hours=24),
    allowable_methods=('GET', 'POST')
)

SEARCH_URL = 'https://report.boonecountymo.org/mrcjava/servlet/RMS01_MP.I00030s?max_rows=10000'


def get_search_results():
    r = requests.get(
        SEARCH_URL,
        headers={'user-agent': "I'm good people!!!"}
    )

    r.raise_for_status()

    return r.content


def extract_details_url(search_results):
    soup = BeautifulSoup(search_results, 'lxml')

    details_urls = []

    table = soup.find('table', class_='collapse data-table shadow responsive')

    tr = table.find('tr', class_='odd')


    url = tr.find('a').attrs['href']


    return url


def get_details(rel_url):

    full_url = 'https://report.boonecountymo.org/mrcjava/servlet/' + rel_url

    r = requests.post(
        full_url,
        headers={'user-agent': "I'm good people!!!"}
    )

    r.raise_for_status()

    return r.content


def extract_details_data(details):
    soup = BeautifulSoup(details, 'lxml')

    detainees_all = soup.find_all('div', class_='detaineeInfo')

    for detainee in detainees_all:
        detainee_info_table = detainee.find('table', class_='collapse centered_table shadow')
        detainee_trs = detainee_info_table.find_all('tr')

        data = {}

        for tr in detainee_trs:
            key = tr.find('td', class_='one td_left').text.lower().strip()
            value = tr.find('td', class_='two td_left').text.strip()

            data[key] = value

        info = Info.create(**data)

def extract_charges_data(details):
    soup = BeautifulSoup(details, 'lxml')

    detainees_charges_all = soup.find_all('div', class_='chargesContainer')

    for detainee_charge in detainees_charges_all:
        detainee_charge_table = detainee_charge.find('table', class_='collapse centered_table shadow responsive')
        detainee_charge_body = detainee_charge_table.find('tbody', class_='single')
        charges_trs = detainee_charge_body.find_all('tr')

        for charges_tr in charges_trs:
            charge_cell = charges_tr.find_all('td', class_='two td_left')

            Charges.create(
                case_number = charge_cell[0].text.strip(),
                charge_description = charge_cell[1].text.strip(),
                charge_status = charge_cell[2].text.strip(),
                bail_amount = charge_cell[3].text.strip(),
                bond_type = charge_cell[4].text.strip(),
                court_date = charge_cell[5].text.strip(),
                court_time = charge_cell[6].text.strip(),
                court_jurisdiction = charge_cell[7].text.strip()
            )


def main():
    search_results = get_search_results()
    details_url = extract_details_url(search_results)
    details_page = get_details(details_url)
    extract_details_data(details_page)
    extract_charges_data(details_page)

    # for url in urls:
    #     details = get_details(url)
    #     sleep(3)


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
