import pandas as pd # type: ignore
from time import time

def limpesa_insercao_dados_silver(engine):
    df_clean = pd.read_csv('SRC/DATA/energiaGlob.csv')
    df_clean = df_clean.drop_duplicates()
    replace_dict = {'@': 'a', '&': 'e', '$': 's'}
    columns_to_fill = [
        "Total Energy Consumption (TWh)",
        "Per Capita Energy Use (kWh)",
        "Renewable Energy Share (%)",
        "Fossil Fuel Dependency (%)",
        "Industrial Energy Use (%)",
        "Household Energy Use (%)",
        "Carbon Emissions (Million Tons)",
        "Energy Price Index (USD/kWh)"
    ]

    collumns_to_check = [
        "Renewable Energy Share (%)",
        "Household Energy Use (%)"
    ]
    df_clean['Country'] = df_clean['Country'].replace(replace_dict, regex=True)
    for col in columns_to_fill:
        df_clean[col] = df_clean.groupby("Country")[col].transform(lambda x: x.fillna(x.median()))
    for col in collumns_to_check:
        df_clean[col] = df_clean[col].clip(0, 100)
    df_clean = df_clean[df_clean["Fossil Fuel Dependency (%)"].between(0, 100)]
    df_clean = df_clean[df_clean["Year"] > 1999]
    df_clean = df_clean.round(4)
    df_clean.to_csv("SRC/DATA/Silver.csv", index=False)

    parte = pd.read_csv('SRC/DATA/Silver.csv', iterator=True, chunksize=1000 )
    while True:
        try:
            t_start = time()
            df = next(parte)
            df.to_sql(name='Silver_Data', con=engine, if_exists='append')
            t_end = time()
            print('uma parte levou %.3f segundos' % (t_end - t_start))
        except StopIteration:
            print("fim dos dados limpos")
            break