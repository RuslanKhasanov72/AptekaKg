from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from g4f.client import Client
from g4f.Provider import Blackbox
import re
linksurl=[]
linksname=[]
linksavailable=[]
linkprice=[]
linksimages=[]
lastpage=1
integer=0
def RemoveEnglish(text):
    # Удаляем все английские буквы (и прописные, и строчные), цифры и символы
    cleaned_text = re.sub(r'[A-Za-z0-9!@#\$%\^\&\*\(\)_\+\-=\[\]\{\};:\'",<>\./?\\|`~]', '', text)
    return cleaned_text
def removesmes(text):
    pattern = re.compile(re.escape("$@$") + r'.*?' + re.escape("$@$"))
    return re.sub(pattern, '', text)

Base = automap_base()
engine = create_engine("postgresql://postgres:qwerty@localhost:5432/Apteka")
Base.prepare(engine)
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
        stock=link.find('span', class_='in-stock')
        print(stock)
        if(stock==None):
            linksavailable.append(link.find('span', class_='out-of-stock'))
        else:
            linksavailable.append(stock)
        linkprice.append(link.find('span', class_='woocommerce-Price-amount amount'))
        linksimages.append(link.find('img',class_='woocommerce-placeholder wp-post-image'))
    print(integer)

    for i, link in enumerate(linksname):
        Medicines = Base.classes.Medicines
        Categories = Base.classes.Categories
        SubCategories = Base.classes.SubCategories
        urlreal = linksurl[i]
        name = linksname[i].text  # извлекаем наименование из блока со ссылкой
        availablebool = False
        available = linksavailable[i].text
        print(available)
        if (available == "В наличии"):
            availablebool = True
        else:
            availablebool = False
        price = linkprice[i].text.replace("\xa0сом", "").replace("от", "").replace(" ","")
        image = linksimages[i].get('src')
        db_session = Session(engine)
        medname = db_session.query(Medicines).filter_by(Name=name, FranchiseId=5).first()
        if (medname == None):
            print('add')
            client = Client()
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                provider=Blackbox,
                messages=[{"role": "user",
                           "content": f"Выбери только одну категорию из предоставленного списка категорий для лекарства {name}. Категории: Антибиотики, Антисептические средства, Антитромботические средства, Болезни крови, Восстановление водно-электролитного баланса, Гормональные препараты, Для печени, Желудочно-кишечный тракт, Женское здоровье, Заболевание нервной системы, Кости и суставы, Лечение алкоголизма и табакокурения, Лечение заболеваний щитовидной железы, Мази, Мужское здоровье, Обезболивающие средства, Обмен веществ, Общеукрепляющие средства, Онкология, От астмы, От паразитов, От сахарного диабета, Отхаркивающие, Плазмозамещающие средства, Почки и мочевыводящие пути, Препараты для лечения глаз, При головных болях, При отравлении и дизентерии, Простуда и грипп, Противовирусные, Противовоспалительные средства, Противогрибковые средства, Противомикробные препараты, Противоопухолевые, Противопедикулезные средства, Ранозаживляющие препараты, Растворители, Рентгеноконтрастное вещество, Сердечно-сосудистые средства, Средства для сна, Средства для лечения геморроя, Средства для полости рта, Средства от аллергии, Средства от кашля, Средства от прыщей, Средства парентерального питания, Препараты для лечения ЛОР-органов, Аппликаторы, Вакуумные банки, Грелки, Защита от вируса, Лабораторные изделия, Одноразовые изделия, Первая помощь, Презервативы и контрацептивы, Товары для реабилитации, Уход за больными, Хирургические инструменты, Хирургические принадлежности, Таблетница, Для гинекологии, Раствор для линз, Бактерицидная лампа, Глюкометры и комплектующие, Ингаляторы, Кислородные концентраторы и их запчасти, Массажеры, Медицинская мебель, Оборудование для дезинфекции и стерилизации, Отсасыватели мокроты, Пульсоксиметры, Ростомер, Слуховой аппарат, Спейсеры, Спирометры, Спорттовары, Стоматологическое оборудование, Термогигрометр, Термометры, Тонометры, Тонометры внутриглазного давления, Физиотерапия, Запчасти и комплектующие, Электрокардиограф, Реанимационный монитор, Витамины и БАДы, Компрессионные изделия, Молокоотсосы, Питание, Уход за грудью, Средства от растяжек, Прокладки после родов, Подушки для кормления, Декоративная косметика, Наборы, Солнцезащитные средства, Уход за волосами, Уход за лицом, Уход за руками и ногами, Уход за телом, Дермокосметика, БАДы, БАДы Витамин+, БАДы Солгар, Витамины и витаминно-минеральные комплексы, Мультивитамины, Витамины для инъекции, Моновитамины, Витамины и БАДы Health&Beauty, Антисептические средства, Ватно-бумажная продукция, Влажные салфетки, Дезодоранты, Депиляция и бритье, Интимная гигиена, Мыло, Ножницы, Уход за полостью рта, Экопрокладки, Для стирки, Листья, Настойки, Плоды, Сборы, Семена, Сиропы и соки лекарственных трав, Травы, Травяные чаи, Цветки, Корни и корневища, Кора, Витамины для детей, Игрушки, Молокоотсосы, Одежда, Питание, При прорезывании зубов, Товары для кормления детей, Уход и гигиена, Электроприборы для детей, Для сна, Для стирки, Трусики после обрезания . Ответ должен быть только одной категорией из списка и ничем больше. Например, если категории: болеутоляющие, противовоспалительные, жаропонижающие, антиагреганты, правильный ответ: 'жаропонижающие'. Неправильный ответ: 'обезболивающие'."}], )
            messageai = RemoveEnglish(response.choices[0].message.content)
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                provider=Blackbox,
                messages=[{"role": "user",
                           "content": f"напиши полное описание для лекарства {name} с тэгами для html внутри div, отправь только код без сторонних сообщений"}], )
            description = removesmes(response.choices[0].message.content)
            cat = db_session.query(SubCategories).filter_by(Name=messageai).first()
            if (cat == None):
                cat = db_session.query(SubCategories).filter_by(Name='Лекарственные средства').first()
                db_session.add(Medicines(URL=urlreal, Name=name, Available=availablebool, Price=price,
                                         Description=''.join(description),
                                         FranchiseId=5, CategoryId=cat.CategoryId, SubCategoryId=cat.Id,
                                         ImageUrl=image))
            else:
                db_session.add(Medicines(URL=urlreal, Name=name, Available=availablebool, Price=price,
                                         Description=''.join(description),
                                         FranchiseId=5, CategoryId=cat.CategoryId, SubCategoryId=cat.Id,
                                         ImageUrl=image))
            db_session.commit()
        else:
            print('update')
            med_to_update = db_session.query(Medicines).filter_by(Name=link.text, FranchiseId=5).first()
            med_to_update.Available = availablebool
            print(availablebool)
            med_to_update.Price = price
            db_session.commit()
        print(f'{i}: {urlreal}')
    linksurl = []
    linksname = []
    linksavailable = []
    linkprice = []
    linksimages = []
#$@$v=v1.20-rv1$@$
#$@$v=undefined-rv1$@$
#df = pd.DataFrame(medicine, columns=['URL', 'Name', 'Available', 'Price'])
#df.to_excel('./Bimed.xlsx', index=False)


