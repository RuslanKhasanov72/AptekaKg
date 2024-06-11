import time
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from bs4 import BeautifulSoup
import requests
from g4f.client import Client
from g4f.Provider import Blackbox
import re
import pandas as pd
allnemanlinks=['https://neman.kg/lekarstvennye-sredstva/page-','https://neman.kg/medicinskie-izdeliya/page-'
,'https://neman.kg/medicinskaya-tehnika/page-','https://neman.kg/dlya-beremennyh-i-mam/page-','https://neman.kg/krasota-i-zdorove/page-',
'https://neman.kg/vitaminy-i-bady-ru/page-','https://neman.kg/lichnaya-gigiena/page-','https://neman.kg/lechebnye-travy/page-',
'https://neman.kg/tovary-dlya-detey/page-']
linksnameandurl=[]
linksavailable=[]
linkprice=[]
linkimages=[]
integer=0
lastpage=None
def RemoveEnglish(text):
    # Удаляем все английские буквы (и прописные, и строчные), цифры и символы
    cleaned_text = re.sub(r'[A-Za-z0-9!@#\$%\^\&\*\(\)_\+\-=\[\]\{\};:\'",<>\./?\\|`~]', '', text)
    return cleaned_text
Base = automap_base()
engine = create_engine("postgresql://postgres:qwerty@localhost:5432/Apteka")
Base.prepare(engine)
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
        links = soup.find_all('div', class_='ut2-gl__body content-on-hover')
        for link in links:
            linkimages.append(link.find('img',class_='ty-pict img-ab-hover-gallery cm-image'))
            linksnameandurl.append(link.find('a', class_='product-title'))
            linksavailable.append(link.find('span', class_='ty-qty-in-stock ty-control-group__item'))
            linkprice.append(link.find('span', class_='ty-price-num',id=True))
        print(integer)
        for g, link in enumerate(linksnameandurl):
            Medicines = Base.classes.Medicines
            Categories = Base.classes.Categories
            SubCategories = Base.classes.SubCategories
            db_session = Session(engine)
            urlmain = linksnameandurl[g].get("href")
            name = linksnameandurl[g].text  # извлекаем наименование из блока со ссылкой
            image=linkimages[g].get('src')
            availablebool = False
            if linksavailable[g] != None:
                available = linksavailable[g].text.replace("\n", "")
                available = available.replace("  ", "")
                if (available == "В наличии"):
                    availablebool = True
                else:
                    availablebool = False
            if linkprice[g] != None:
                price = linkprice[g].text.replace("\u200d", "")
            else:
                price=-1
            medname = db_session.query(Medicines).filter_by(Name=link.text, FranchiseId=18).first()
            if (medname==None):
                print('add')
                try:
                    htmlmain = requests.get(urlmain).text
                except:
                    time.sleep(5)
                    htmlmain = requests.get(urlmain).text
                soupmain = BeautifulSoup(htmlmain, 'html.parser')
                description = soupmain.find('div', class_='ty-wysiwyg-content content-description').decode_contents()
                category = soupmain.find_all('a', class_='ty-breadcrumbs__a')
                catnumber=len(category)
                if (catnumber>2):
                    categoryname=''.join(category[2].text)
                    cat = db_session.query(SubCategories).filter_by(Name=categoryname).first()
                    db_session.add(Medicines(URL=urlmain, Name=name, Available=availablebool, Price=price, Description=''.join(description),
                                         FranchiseId=18, CategoryId=cat.CategoryId, SubCategoryId=cat.Id,ImageUrl=image))
                    db_session.commit()
                else:
                    client = Client()
                    response = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        provider=Blackbox,
                        messages=[{"role": "user", "content": f"Выбери только одну категорию из предоставленного списка категорий для лекарства {name}. Категории: Антибиотики, Антисептические средства, Антитромботические средства, Болезни крови, Восстановление водно-электролитного баланса, Гормональные препараты, Для печени, Желудочно-кишечный тракт, Женское здоровье, Заболевание нервной системы, Кости и суставы, Лечение алкоголизма и табакокурения, Лечение заболеваний щитовидной железы, Мази, Мужское здоровье, Обезболивающие средства, Обмен веществ, Общеукрепляющие средства, Онкология, От астмы, От паразитов, От сахарного диабета, Отхаркивающие, Плазмозамещающие средства, Почки и мочевыводящие пути, Препараты для лечения глаз, При головных болях, При отравлении и дизентерии, Простуда и грипп, Противовирусные, Противовоспалительные средства, Противогрибковые средства, Противомикробные препараты, Противоопухолевые, Противопедикулезные средства, Ранозаживляющие препараты, Растворители, Рентгеноконтрастное вещество, Сердечно-сосудистые средства, Средства для сна, Средства для лечения геморроя, Средства для полости рта, Средства от аллергии, Средства от кашля, Средства от прыщей, Средства парентерального питания, Препараты для лечения ЛОР-органов, Аппликаторы, Вакуумные банки, Грелки, Защита от вируса, Лабораторные изделия, Одноразовые изделия, Первая помощь, Презервативы и контрацептивы, Товары для реабилитации, Уход за больными, Хирургические инструменты, Хирургические принадлежности, Таблетница, Для гинекологии, Раствор для линз, Бактерицидная лампа, Глюкометры и комплектующие, Ингаляторы, Кислородные концентраторы и их запчасти, Массажеры, Медицинская мебель, Оборудование для дезинфекции и стерилизации, Отсасыватели мокроты, Пульсоксиметры, Ростомер, Слуховой аппарат, Спейсеры, Спирометры, Спорттовары, Стоматологическое оборудование, Термогигрометр, Термометры, Тонометры, Тонометры внутриглазного давления, Физиотерапия, Запчасти и комплектующие, Электрокардиограф, Реанимационный монитор, Витамины и БАДы, Компрессионные изделия, Молокоотсосы, Питание, Уход за грудью, Средства от растяжек, Прокладки после родов, Подушки для кормления, Декоративная косметика, Наборы, Солнцезащитные средства, Уход за волосами, Уход за лицом, Уход за руками и ногами, Уход за телом, Дермокосметика, БАДы, БАДы Витамин+, БАДы Солгар, Витамины и витаминно-минеральные комплексы, Мультивитамины, Витамины для инъекции, Моновитамины, Витамины и БАДы Health&Beauty, Антисептические средства, Ватно-бумажная продукция, Влажные салфетки, Дезодоранты, Депиляция и бритье, Интимная гигиена, Мыло, Ножницы, Уход за полостью рта, Экопрокладки, Для стирки, Листья, Настойки, Плоды, Сборы, Семена, Сиропы и соки лекарственных трав, Травы, Травяные чаи, Цветки, Корни и корневища, Кора, Витамины для детей, Игрушки, Молокоотсосы, Одежда, Питание, При прорезывании зубов, Товары для кормления детей, Уход и гигиена, Электроприборы для детей, Для сна, Для стирки, Трусики после обрезания . Ответ должен быть только одной категорией из списка и ничем больше. Например, если категории: болеутоляющие, противовоспалительные, жаропонижающие, антиагреганты, правильный ответ: 'жаропонижающие'. Неправильный ответ: 'обезболивающие'."}],)
                    messageai=RemoveEnglish(response.choices[0].message.content)
                    print(messageai)
                    cat = db_session.query(SubCategories).filter_by(Name=messageai).first()
                    if(cat==None):
                        cat = db_session.query(SubCategories).filter_by(Name='Лекарственные средства').first()
                        db_session.add(Medicines(URL=urlmain, Name=name, Available=availablebool, Price=price,
                                                 Description=''.join(description),
                                                 FranchiseId=18, CategoryId=cat.CategoryId, SubCategoryId=cat.Id,
                                                 ImageUrl=image))
                    else:
                        db_session.add(Medicines(URL=urlmain, Name=name, Available=availablebool, Price=price,
                                             Description=''.join(description),
                                             FranchiseId=18, CategoryId=cat.CategoryId, SubCategoryId=cat.Id,ImageUrl=image))
                    db_session.commit()
            else:
                print('update')
                med_to_update = db_session.query(Medicines).filter_by(Name=link.text, FranchiseId=18).first()
                med_to_update.Available = availablebool
                med_to_update.Price = price
                db_session.commit()
            print(f'{g}: {urlmain}')
        linksnameandurl = []
        linksavailable = []
        linkprice = []
        linkimages=[]
    integer = 0
    lastpage = None



#df = pd.DataFrame(medicine, columns=['URL', 'Name', 'Available', 'Price','Description','SubCategory'])
#df.to_excel('./Neman.xlsx', index=False)



