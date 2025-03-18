import pandas as pd # type: ignore
from sqlalchemy import create_engine # type: ignore
from time import time

df = pd.read_csv("global_energy_consumption.csv")
con = create_engine('postgresql://root:root@localhost:5432/energia_glob')
pd.io.sql.get_schema(df, name='tes2', con=con)
df.head(n=0).to_sql(name='tes2', con=con, if_exists='replace')

pt = pd.read_csv("global_energy_consumption.csv", iterator=True, chunksize=50)

while True:
    ts = time()
    df= next(pt)
    df.to_sql(name='tes2', con=con, if_exists='append')
    te= time()
    print ('tempo: %.3f' % (ts - te))