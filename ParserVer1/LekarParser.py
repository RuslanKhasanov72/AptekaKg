from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
import pandas as pd
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from g4f.client import Client
from g4f.Provider import Blackbox
import requests
import re
def RemoveEnglish(text):
    # Удаляем все английские буквы (и прописные, и строчные), цифры и символы
    cleaned_text = re.sub(r'[A-Za-z0-9!@#\$%\^\&\*\(\)_\+\-=\[\]\{\};:\'",<>\./?\\|`~]', '', text)
    return cleaned_text
def removesmes(text):
    pattern = re.compile(re.escape("$@$") + r'.*?' + re.escape("$@$"))
    return re.sub(pattern, '', text)
driver = webdriver.Chrome()
driver.get('https://lekar.kg/katalog/')
stop=0
while 1:
    try:
        elem = driver.find_element(By.XPATH, '//*[@id="b5691"]/section/div/div/div/div/div/div/div[2]/button')
    except:
        break
    if elem.text=="Показать ещё":
        elem.click()
        time.sleep(2)

Base = automap_base()
engine = create_engine("postgresql://postgres:qwerty@localhost:5432/Apteka")
Base.prepare(engine)
linksnameandurl=[]
linkprice=[]
medicine=[]
source=(driver.page_source)
soup = BeautifulSoup(source, 'html.parser')
links = soup.find_all('div', class_='col-6 col-md-3 product-item-small-card')
for link in links:
    linksnameandurl.append(link.find('h3', class_='product-item-title'))
    linkprice.append(link.find('span', class_='product-item-price-current', id=True))

for i, link in enumerate(linksnameandurl):
    url = linksnameandurl[i].find("a")  # получаем ссылку товара
    urlreal=url.get('href')
    name = linksnameandurl[i].text.replace("\t","").replace("\n","")  # извлекаем наименование из блока со ссылкой
    price = re.sub(r'\D', '', linkprice[i].text)
    Medicines = Base.classes.Medicines
    Categories = Base.classes.Categories
    SubCategories = Base.classes.SubCategories
    db_session = Session(engine)
    medname = db_session.query(Medicines).filter_by(Name=name, FranchiseId=19).first()
    if (medname == None):
        print('add')
        try:
            htmlmain = requests.get(urlreal).text
        except:
            time.sleep(5)
            htmlmain = requests.get(urlreal).text
        soupmain = BeautifulSoup(htmlmain, 'html.parser')
        imagediv = soupmain.find('div', class_='product-detail-slider-image')
        image=soupmain.find('img').get('src')
        client = Client()
        try:
            description=soupmain.find('div', class_='product-item-detail-tab-content active').decode_contents()
        except:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                provider=Blackbox,
                messages=[{"role": "user",
                           "content": f"напиши полное описание для лекарства {name} с тэгами для html внутри div, отправь только код без сторонних сообщений"}], )
            description = removesmes(response.choices[0].message.content)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            provider=Blackbox,
            messages=[{"role": "user",
                       "content": f"Выбери только одну категорию из предоставленного списка категорий для лекарства {name}. Категории: Антибиотики, Антисептические средства, Антитромботические средства, Болезни крови, Восстановление водно-электролитного баланса, Гормональные препараты, Для печени, Желудочно-кишечный тракт, Женское здоровье, Заболевание нервной системы, Кости и суставы, Лечение алкоголизма и табакокурения, Лечение заболеваний щитовидной железы, Мази, Мужское здоровье, Обезболивающие средства, Обмен веществ, Общеукрепляющие средства, Онкология, От астмы, От паразитов, От сахарного диабета, Отхаркивающие, Плазмозамещающие средства, Почки и мочевыводящие пути, Препараты для лечения глаз, При головных болях, При отравлении и дизентерии, Простуда и грипп, Противовирусные, Противовоспалительные средства, Противогрибковые средства, Противомикробные препараты, Противоопухолевые, Противопедикулезные средства, Ранозаживляющие препараты, Растворители, Рентгеноконтрастное вещество, Сердечно-сосудистые средства, Средства для сна, Средства для лечения геморроя, Средства для полости рта, Средства от аллергии, Средства от кашля, Средства от прыщей, Средства парентерального питания, Препараты для лечения ЛОР-органов, Аппликаторы, Вакуумные банки, Грелки, Защита от вируса, Лабораторные изделия, Одноразовые изделия, Первая помощь, Презервативы и контрацептивы, Товары для реабилитации, Уход за больными, Хирургические инструменты, Хирургические принадлежности, Таблетница, Для гинекологии, Раствор для линз, Бактерицидная лампа, Глюкометры и комплектующие, Ингаляторы, Кислородные концентраторы и их запчасти, Массажеры, Медицинская мебель, Оборудование для дезинфекции и стерилизации, Отсасыватели мокроты, Пульсоксиметры, Ростомер, Слуховой аппарат, Спейсеры, Спирометры, Спорттовары, Стоматологическое оборудование, Термогигрометр, Термометры, Тонометры, Тонометры внутриглазного давления, Физиотерапия, Запчасти и комплектующие, Электрокардиограф, Реанимационный монитор, Витамины и БАДы, Компрессионные изделия, Молокоотсосы, Питание, Уход за грудью, Средства от растяжек, Прокладки после родов, Подушки для кормления, Декоративная косметика, Наборы, Солнцезащитные средства, Уход за волосами, Уход за лицом, Уход за руками и ногами, Уход за телом, Дермокосметика, БАДы, БАДы Витамин+, БАДы Солгар, Витамины и витаминно-минеральные комплексы, Мультивитамины, Витамины для инъекции, Моновитамины, Витамины и БАДы Health&Beauty, Антисептические средства, Ватно-бумажная продукция, Влажные салфетки, Дезодоранты, Депиляция и бритье, Интимная гигиена, Мыло, Ножницы, Уход за полостью рта, Экопрокладки, Для стирки, Листья, Настойки, Плоды, Сборы, Семена, Сиропы и соки лекарственных трав, Травы, Травяные чаи, Цветки, Корни и корневища, Кора, Витамины для детей, Игрушки, Молокоотсосы, Одежда, Питание, При прорезывании зубов, Товары для кормления детей, Уход и гигиена, Электроприборы для детей, Для сна, Для стирки, Трусики после обрезания . Ответ должен быть только одной категорией из списка и ничем больше. Например, если категории: болеутоляющие, противовоспалительные, жаропонижающие, антиагреганты, правильный ответ: 'жаропонижающие'. Неправильный ответ: 'обезболивающие'."}], )
        messageai = RemoveEnglish(response.choices[0].message.content)
        print(messageai)
        cat = db_session.query(SubCategories).filter_by(Name=messageai).first()
        if (cat == None):
            cat = db_session.query(SubCategories).filter_by(Name='Лекарственные средства').first()
            db_session.add(Medicines(URL=urlreal, Name=name, Available=True, Price=price,
                                     Description=''.join(description),
                                     FranchiseId=19, CategoryId=cat.CategoryId, SubCategoryId=cat.Id,
                                     ImageUrl=image))
        else:
            db_session.add(Medicines(URL=urlreal, Name=name, Available=True, Price=price,
                                     Description=''.join(description),
                                     FranchiseId=19, CategoryId=cat.CategoryId, SubCategoryId=cat.Id, ImageUrl=image))
        db_session.commit()
    else:
        print('update')
        med_to_update = db_session.query(Medicines).filter_by(Name=name, FranchiseId=19).first()
        med_to_update.Available = True
        med_to_update.Price = price
        db_session.commit()
    print(f'{i}: {urlreal}')

