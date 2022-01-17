from bs4 import BeautifulSoup
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

    price = doc.select('button[class="LkLjZd ScJHi HPiPcc IfEcue"]  meta[itemprop="price"]')[0]['content'].replace('$','')
    price2 = float(price) * 14266.00
    price_final = 'Rp ' + "{:,}".format(int(price2)) + ',00'

    rating = doc.find('div', class_='BHMmbe').text

    total_rating = doc.find('span', class_='EymY4b').text
    
    
    scrap_data = {
        'cover':cover_final,
        'title':title,
        'descr':description,
        'author':author,
        'publisher':publisher,
        'pub_date':publication_date,
        'genres':genres,
        'lang':language,
        'pages':pages,
        'comp':compability,
        'price':price_final,
        'rat':rating,
        'tot_rat':total_rating
    }

    return scrap_data
