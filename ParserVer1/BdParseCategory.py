from bs4 import BeautifulSoup
import requests
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
import time
allnemanlinks=['https://neman.kg/lekarstvennye-sredstva/page-','https://neman.kg/medicinskie-izdeliya/page-'
,'https://neman.kg/medicinskaya-tehnika/page-','https://neman.kg/dlya-beremennyh-i-mam/page-','https://neman.kg/krasota-i-zdorove/page-',
'https://neman.kg/vitaminy-i-bady-ru/page-','https://neman.kg/lichnaya-gigiena/page-','https://neman.kg/lechebnye-travy/page-',
'https://neman.kg/tovary-dlya-detey/page-']
subcategories= []
categories=[]
finallist=[]
for link in allnemanlinks:
    link = f'{link}1'
    try:
        html = requests.get(link).text
    except:
        time.sleep(5)
        html = requests.get(link).text
    soup = BeautifulSoup(html, 'html.parser')
    category = soup.find('li', class_='ut2-item level-0 ut2-current-item').text
    categories.append(category)
    subcategories=soup.find_all('li', class_='ut2-item level-1')

    for subcategory in subcategories:
        finallist.append([category.replace("\n",""),subcategory.text.replace("\n","")])

print(finallist)

Base = automap_base()
engine = create_engine("postgresql://postgres:qwerty@localhost:5432/Apteka")
Base.prepare(engine)
Categories = Base.classes.Categories
SubCategories = Base.classes.SubCategories
db_session = Session(engine)
for item in finallist:
    cat = db_session.query(Categories).filter_by(Name=''.join(item[0])).first()
    db_session.add(SubCategories(Name=''.join(item[1]), CategoryId=cat.Id))

#for item in categories:
    #db_session.add(Categories(Name=item))
db_session.commit()