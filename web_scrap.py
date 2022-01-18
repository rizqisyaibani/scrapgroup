from bs4 import BeautifulSoup
from datetime import datetime

import requests
import re

def scrape_func(url):
    
    result = requests.get(url).text
    doc = BeautifulSoup(result, "html.parser")

    cover = doc.find('img', class_="T75of h1kAub")
    cover_final = cover['src']

    title = doc.find('h1', class_='AHFaub').text

    description = doc.find('div', class_='DWPxHb').text

    author = doc.find('a', class_='hrTbp R8zArc').text

    publisher = doc.find('div', string='Publisher').find_next_sibling().text

    publication_date = doc.find("div", string='Published on').find_next_sibling().text

    genres = doc.find("div", string='Genres').find_next_sibling().text

    language = doc.find('div', string='Language').find_next_sibling().text

    pages = doc.find('div', string='Pages').find_next_sibling().text

    compability = doc.find("div", string='Best for').find_next_sibling().text

    price = doc.find_all("button", jsmodel="UfnShf")[0]
    price2 = float(price.getText().replace(' Ebook', '').replace('$', '').split(' ')[-1]) * 14266.00
    price_final = 'Rp ' + '{:.2f}'.format(price2)

    rating = doc.find('div', class_='BHMmbe').text

    total_rating = doc.find('span', class_='EymY4b').text
    
    
    scrap_data = {
        'cover':cover_final,
        'title':title,
        'descr':description,
        'author':author,
        'publisher':publisher,
        'pub_date':get_datetime(publication_date),
        'genres':genres,
        'lang':language,
        'pages':pages,
        'comp':compability,
        'price':price_final.replace('Rp',''),
        'rat':rating,
        'tot_rat':total_rating
    }

    return scrap_data

def get_datetime(d):
    list_d = d.split(" ")
    date = int(list_d[1].replace(',', ''))
    month_list = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    month = month_list.index(list_d[0]) + 1
    year = int(list_d[2])

    return datetime(year, month, date)