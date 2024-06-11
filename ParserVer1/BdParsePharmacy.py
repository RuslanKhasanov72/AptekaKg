from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
import pandas as pd

df = pd.read_excel('../.././Apt24.xlsx',skiprows=1)

# Извлечение второго и третьего столбцов
firms_and_addresses = df.iloc[:, [1,2]]

# Переименование столбцов для удобства
firms_and_addresses.columns = ['Фирма', 'Адрес']

# Удаление строк, в которых все значения пропущены
firms_and_addresses = firms_and_addresses.dropna(how='all')

# Заполнение пропущенных значений в столбце 'Фирма' предыдущими ненулевыми значениями
firms_and_addresses['Фирма'] = firms_and_addresses['Фирма'].ffill()
firm_address_list = firms_and_addresses.values.tolist()

# Печать результатов


Base = automap_base()
engine = create_engine("postgresql://postgres:qwerty@localhost:5432/Apteka")
Base.prepare(engine)
Franchises = Base.classes.Franchises
Pharmacies = Base.classes.Pharmacies
db_session = Session(engine)
for item in firm_address_list:
    firm = db_session.query(Franchises).filter_by(Name=item[0]).first()
    if firm:
        print(firm.Id)
for item in firm_address_list:
    firm = db_session.query(Franchises).filter_by(Name=item[0]).first()
    db_session.add(Pharmacies(FranchiseId=firm.Id,Address=item[1],Number='1'))
db_session.commit()

