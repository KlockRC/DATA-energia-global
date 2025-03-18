import pandas as pd # type: ignore
from sqlalchemy import create_engine # type: ignore
from time import time

df = pd.read_csv('global_energy_consumption.csv', nrows=10)
engine = create_engine('postgresql://root:root@localhost:5432/energia_glob')
pd.io.sql.get_schema(df, name="energia_global",con=engine)
df.head(n=0).to_sql(name="energia_global", con=engine, if_exists='replace')

parte = pd.read_csv('global_energy_consumption.csv', iterator=True, chunksize=100 )

while True:
    t_start = time()
    df = next(parte)
    df.to_sql(name='energia_global', con=engine, if_exists='append')
    t_end = time()
    print('mais uma parte levou %.3f segundos' % (t_end - t_start))