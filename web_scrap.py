from bs4 import BeautifulSoup
import requests
import re

url = "https://play.google.com/store/books/details/H_G_Wells_The_Time_Machine_Illustrated_edition?id=C11ODwAAQBAJ"

result = requests.get(url)
doc = BeautifulSoup(result.text,"html.parser")


cover = doc.find('img', class_="T75of h1kAub")
cover2 = cover['src']

title = doc.find('h1', class_='AHFaub').text

description = doc.find('div', class_='DWPxHb').text

author = doc.find('a', class_='hrTbp R8zArc').text

publisher = doc.find('div', string='Publisher').find_next_sibling().text

publication_date = doc.find("div", string='Published on').find_next_sibling().text

genres = doc.find("div", string='Genres').find_next_sibling().text

language = doc.find('div', string='Language').find_next_sibling().text

pages = doc.find('div', string='Pages').find_next_sibling().text

compability = doc.find("div", string='Best for').find_next_sibling().text

harga = doc.select('button[class="LkLjZd ScJHi HPiPcc IfEcue"]  meta[itemprop="price"]')[0]['content'].replace('$','')
harga2 = float(harga) * 14266.00
harga_final = 'Rp ' + "{:,}".format(int(harga2)) + ',00'

rating = doc.find('div', class_='BHMmbe').text

total_rating = doc.find('span', class_='EymY4b').text


print(harga_final)


    url = "https://play.google.com/store/books/details/H_G_Wells_The_Time_Machine_Illustrated_edition?id=C11ODwAAQBAJ"
    result = requests.get(url)
    doc = BeautifulSoup(result.text,"html.parser")

    cover = doc.find('img', class_="T75of h1kAub")
    cover2 = cover['src']

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
    final_price = 'Rp ' + "{:,}".format(int(price2)) + ',00'

    rating = doc.find('div', class_='BHMmbe').text

    total_rating = doc.find('span', class_='EymY4b').text
    