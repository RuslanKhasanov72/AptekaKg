from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
linksurl=[]
linksname=[]
linksavailable=[]
linkprice=[]
lastpage=1
integer=0
medicine=[]
while lastpage!=None:
    integer=integer+1
    link=f"https://bimed.kg/shop/page/{integer}/"
    try:
        html = requests.get(link).text
    except:
        time.sleep(10)
        html = requests.get(link).text
    soup = BeautifulSoup(html, 'html.parser')
    lastpage = soup.find('a', class_='next page-numbers')
    links = soup.find_all('a', class_='woocommerce-LoopProduct-link woocommerce-loop-product__link')
    for link in links:
        linksurl.append(link.get("href"))
        linksname.append(link.find('h2', class_='woocommerce-loop-product__title'))
        linksavailable.append(link.find('span', class_='in-stock'))
        linkprice.append(link.find('span', class_='woocommerce-Price-amount amount'))

for i, link in enumerate(linksname): # получаем ссылку товара
    name = linksname[i].text  # извлекаем наименование из блока со ссылкой
    available=linksavailable[i].text
    price = linkprice[i].text.replace("\xa0сом","").replace("от","")
    medicine.append([linksurl[i],name,available,price])
    print(medicine[i])

df = pd.DataFrame(medicine, columns=['URL', 'Name', 'Available', 'Price'])
df.to_excel('./Bimed.xlsx', index=False)