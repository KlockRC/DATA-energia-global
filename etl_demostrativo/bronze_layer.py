import pandas as pd  # type: ignore
from time import time

def bronze_inserir_no_db(engine):
    parte = pd.read_csv('s3://data-energia-global/energiaGlob.csv', storage_options={"anon": True}, iterator=True, chunksize=1000 )
    while True:
        try:
            t_start = time()
            df = next(parte)
            df.to_sql(name='tese_data', con=engine, if_exists='append')
            t_end = time()
            print('uma parte levou %.3f segundos' % (t_end - t_start))
        except StopIteration:
            print("fim dos dados")
            break


