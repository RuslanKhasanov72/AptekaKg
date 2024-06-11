from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
import pandas as pd

df = pd.read_excel('../.././Apt24.xlsx',skiprows=1)

# Извлечение второго и третьего столбцов
firms_and_addresses = df.iloc[:, [1]]

# Переименование столбцов для удобства
firms_and_addresses.columns = ['Фирма']

# Удаление строк, в которых все значения пропущены
firms_and_addresses = firms_and_addresses.dropna(how='all')

# Заполнение пропущенных значений в столбце 'Фирма' предыдущими ненулевыми значениями
firms_and_addresses['Фирма'] = firms_and_addresses['Фирма'].ffill()
firm_address_list = firms_and_addresses.values.tolist()
for item in firm_address_list:
    print(''.join(item))
Base = automap_base()
engine = create_engine("postgresql://postgres:qwerty@localhost:5432/Apteka")
Base.prepare(engine)
Franchises = Base.classes.Franchises
db_session = Session(engine)
for item in firm_address_list:
    db_session.add(Franchises(Name=''.join(item[0])))
db_session.commit()