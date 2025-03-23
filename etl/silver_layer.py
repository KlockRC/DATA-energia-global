import pandas as pd # type: ignore
from time import time

def limpesa_insercao_dados_silver(engine):
    df_clean = pd.read_sql_table('Bronze_Data', con=engine)
    df_clean = df_clean.drop_duplicates()
    
    df_clean.columns = df_clean.columns.str.replace('/', '-', regex=False)
    df_clean.columns = df_clean.columns.str.replace(' ', '_')

    replace_dict = {'@': 'a', '&': 'e'}
    columns_to_fill = [
        'Total_Energy_Consumption_(TWh)',
        'Per_Capita_Energy_Use_(kWh)',
        'Renewable_Energy_Share_(%)',
        'Fossil_Fuel_Dependency_(%)',
        'Industrial_Energy_Use_(%)',
        'Household_Energy_Use_(%)',
        'Carbon_Emissions_(Million_Tons)',
        'Energy_Price_Index_(USD-kWh)'
    ]

    collumns_to_check = [
        'Renewable_Energy_Share_(%)',
        'Household_Energy_Use_(%)'
    ]
    df_clean['Country'] = df_clean['Country'].replace(replace_dict, regex=True)
    for col in columns_to_fill:
        df_clean[col] = df_clean.groupby("Country")[col].transform(lambda x: x.fillna(x.median()))
    for col in collumns_to_check:
        df_clean[col] = df_clean[col].clip(0, 100)
    df_clean = df_clean.groupby([ "Country","Year"])[columns_to_fill].mean().reset_index()
    df_clean = df_clean[df_clean["Fossil_Fuel_Dependency_(%)"].between(0, 100)]
    df_clean = df_clean[df_clean["Year"] > 1999]
    df_clean = df_clean.round(4)
    df_clean.to_csv("SRC/DATA/SILVER/Silver.csv", index=False)
    df_clean.to_sql(name='Silver_Data', con=engine, if_exists='append')
    unico = df_clean['Country'].unique()
    for uni in unico:
        df = df_clean.groupby("Country").get_group(uni).reset_index()
        df_noindex = df.drop('index', axis=1)
        df_noindex.to_csv(f'SRC/DATA/SILVER/{uni}_silver.csv', index=False)
        df.to_sql(name=f'{uni}_silver', con=engine, if_exists='append')


   