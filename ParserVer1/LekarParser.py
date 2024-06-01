from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
import pandas as pd


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
    price = linkprice[i].text.replace("\t","").replace("\n","")
    medicine.append([urlreal,name,price])

df = pd.DataFrame(medicine, columns=['URL', 'Name', 'Price'])
df.to_excel('./Lekar.xlsx', index=False)