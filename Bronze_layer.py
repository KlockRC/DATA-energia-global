import pandas as pd 
from sqlalchemy import create_engine 
from time import time

df = pd.read_csv('SRC/DATA/energiaGlob.csv')
engine = create_engine('postgresql://root:GlobE@localhost:5433/energia_glob')
pd.io.sql.get_schema(df, name="energia_global",con=engine)
df.to_csv("SRC/DATA/Bronze.csv", index=False)

parte = pd.read_csv('SRC/DATA/energiaGlob.csv', iterator=True, chunksize=1000 )

while True:
    try:
        t_start = time()
        df = next(parte)
        df.to_sql(name='Bronze_Data', con=engine, if_exists='append')
        t_end = time()
        print('uma parte levou %.3f segundos' % (t_end - t_start))
    except StopIteration:
        print("fim dos dados")
        break