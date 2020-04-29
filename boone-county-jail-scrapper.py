#!/usr/bin/env python
# coding: utf-8

import requests


url = 'https://report.boonecountymo.org/mrcjava/servlet/RMS01_MP.I00030s'


r = requests.get(
    "https://report.boonecountymo.org/mrcjava/servlet/RMS01_MP.I00030s",
    params={"max_rows": 10000},
    headers={'user-agent': "I'm good people!!!"}
)


type(r)


r.ok


r.status_code


r.reason


dir(r)


r.content


post_r = requests.post(url, params={'rls_lastname': 'C0'})


post_r.ok


type(r.content)


type(r.text)


r.text


with open ('search-results.html', 'w') as f:
    f.write(r.text)


from bs4 import BeautifulSoup


soup = BeautifulSoup(r.text)


type(soup)


table = soup.find('table', class_= 'collapse data-table shadow responsive')


type(table)


table


table.find_all('th')


th_all = table.find('thead').find_all('tr')[1].find_all('th')


th_all


type(th_all)


for th in th_all:
    print(th.text)


headers = []


for th in th_all:
    header = th.text.strip().replace(' ', '_').lower()
    headers.append(header)


headers


tr_all = table.find_all('tr')[2:183]


for tr in tr_all:
    for td in tr.find_all('td'):
        print(td.text.strip())
    print('---------------')


def clean_row(tds):
    return tds


for tr in tr_all:
    print('--------------')
    tds = tr.find_all('td')
    row = clean_row(tds)
    print(row)


def clean_row(tds):
    row = {
        'details_url': tds[9].find('a').attrs['href'],
        'last_name': tds[0].text.strip(),
        'first_name': tds[1].text.strip(),
        'middle_name': tds[2].text.strip(),
        'suffix': tds[3].text.strip(),
        'sex': tds[4].text.strip(),
        'race': tds[5].text.strip(),
        'age': int(tds[6].text.strip()),
        'city': tds[7].text.strip(),
        'state': tds[8].text.strip()
    }
    return row


rows = []


for tr in tr_all:
    tds = tr.find_all('td')
    row = clean_row(tds)
    rows.append(row)


rows


import csv


rows[0].keys()


with open('jail.csv', 'w', newline='') as f:
    writer = csv.DictWriter(
        f, fieldnames=rows[0].keys()
    )
    
    writer.writeheader()
    for row in rows:
        writer.writerow(row)




