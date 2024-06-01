import time

from bs4 import BeautifulSoup
import requests
import pandas as pd
allnemanlinks=['https://neman.kg/lekarstvennye-sredstva/page-','https://neman.kg/medicinskie-izdeliya/page-'
,'https://neman.kg/medicinskaya-tehnika/page-','https://neman.kg/dlya-beremennyh-i-mam/page-','https://neman.kg/krasota-i-zdorove/page-',
'https://neman.kg/vitaminy-i-bady-ru/page-','https://neman.kg/lichnaya-gigiena/page-','https://neman.kg/lechebnye-travy/page-',
'https://neman.kg/tovary-dlya-detey/page-']
linksnameandurl=[]
linksavailable=[]
linkprice=[]
integer=0
lastpage=None
medicine=[]
for i in allnemanlinks:
    while(lastpage==None):
        integer=integer+1;
        link=f'{i}{integer}'
        try:
            html = requests.get(link).text
        except:
            time.sleep(5)
            html = requests.get(link).text
        soup = BeautifulSoup(html, 'html.parser')
        lastpage = soup.find('a', class_='ty-pagination__item ty-pagination__btn ty-pagination__right-arrow')
        links = soup.find_all('div', class_='ut2-gl__content content-on-hover')
        for link in links:
            linksnameandurl.append(link.find('a', class_='product-title'))
            linksavailable.append(link.find('span', class_='ty-qty-in-stock ty-control-group__item'))
            linkprice.append(link.find('span', class_='ty-price-num',id=True))
        print(integer)



    for i, link in enumerate(linksnameandurl):
        url = linksnameandurl[i].get("href")  # получаем ссылку товара
        name = linksnameandurl[i].text  # извлекаем наименование из блока со ссылкой
        if linksavailable[i]!=None:
            available=linksavailable[i].text.replace("\n","")
            available=available.replace("  ","")
        if linkprice[i] != None:
            price = linkprice[i].text.replace("\u200d","")
        medicine.append([url,name,available,price])
        print(medicine[i])
    integer = 0
    linksnameandurl = []
    linksavailable = []
    linkprice = []
    lastpage = None

df = pd.DataFrame(medicine, columns=['URL', 'Name', 'Available', 'Price'])
df.to_excel('./Neman.xlsx', index=False)
