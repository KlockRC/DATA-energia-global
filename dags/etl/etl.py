import pandas  # type: ignore
from time import time
from sqlalchemy import create_engine  # type: ignore
import os
# Obtenha as variáveis de ambiente do docker-compose
DB_USER = os.environ.get("POSTGRES_USER")
DB_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
DB_HOST = os.environ.get("POSTGRES_HOST")
DB_PORT = os.environ.get("POSTGRES_PORT")
DB_NAME = os.environ.get("POSTGRES_DB")
CSV = os.environ.get("CSV_S3")
endpoint = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

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
replace_dict = {'@': 'a', '&': 'e'}
    
collumns_to_check = [
        'Renewable_Energy_Share_(%)',
        'Household_Energy_Use_(%)'
    ]

engine = create_engine(endpoint)

def bronze_inserir_no_db():  
    parte = pandas.read_csv(CSV, storage_options={"anon": True}, iterator=True, chunksize=1000 )
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
      

def silver_limpesa_insercao_dados_silver():

    df_clean = pandas.read_sql_table('Bronze_Data', con=engine)
    df_clean = df_clean.drop_duplicates()
    
    df_clean.columns = df_clean.columns.str.replace('/', '-', regex=False)
    df_clean.columns = df_clean.columns.str.replace(' ', '_')


    df_clean['Country'] = df_clean['Country'].replace(replace_dict, regex=True)
    for col in columns_to_fill:
        df_clean[col] = df_clean.groupby("Country")[col].transform(lambda x: x.fillna(x.median()))
    for col in collumns_to_check:
        df_clean[col] = df_clean[col].clip(0, 100)

    #arquivos separados
    df_clean = df_clean.groupby([ "Country","Year"])[columns_to_fill].mean().reset_index()
    df_clean = df_clean[df_clean["Fossil_Fuel_Dependency_(%)"].between(0, 100)]
    df_clean = df_clean[df_clean["Year"] > 1999]
    df_clean = df_clean.round(4)
    df_clean.to_sql(name='Silver_Data', con=engine, if_exists='append', index=True)
    unico = df_clean['Country'].unique()
    for uni in unico:
        df = df_clean.groupby("Country").get_group(uni).reset_index()
        df_noindex = df.drop('index', axis=1)
        df.to_sql(name=f'{uni}_silver', con=engine, if_exists='append')

def gold_trasformacao_insercao_dados_gold():

    t_start = time()
    df_gold = pandas.read_sql_table('Silver_Data', con=engine)
    for col in columns_to_fill:
        media_unica_por_pais = df_gold.groupby(["Country"])[col].mean().reset_index()
        media_unica_por_pais = media_unica_por_pais.round(4)
        media_unica_por_pais.to_sql(name=f'media_{col}_por_pais_Gold', con=engine, if_exists='append')

    for col in columns_to_fill:
        df_inicio = df_gold.groupby("Country").first().reset_index()
        df_fim = df_gold.groupby("Country").last().reset_index()

        df_crescimento = df_inicio[["Country", col]].merge(
            df_fim[["Country", col]], on="Country", suffixes=("-inicio", "-fim")
        )

        df_crescimento["Crescimento (%)"] = ((df_crescimento[f"{col}-fim"] - df_crescimento[f"{col}-inicio"]) / df_crescimento[f"{col}-inicio"]) * 100
        df_crescimento = df_crescimento.sort_values("Crescimento (%)", ascending=False)
        df_crescimento = df_crescimento.round(4)
        df_crescimento.to_sql(name=f'crescimento_{col}_Gold', con=engine, if_exists='append')


#---------------------------------------------------------------------------------------------------------------------------------------#
    df_combined = pandas.DataFrame(index=df_gold["Country"].unique())
    for col in columns_to_fill:
        media_por_pais = df_gold.groupby("Country")[col].mean()
        df_combined[f"media_{col}"] = media_por_pais
        df_inicio = df_gold.groupby("Country", as_index=True).first()[col]
        df_fim = df_gold.groupby("Country", as_index=True).last()[col]
        
        df_combined[f"Crescimento (%)_{col}"] = ((df_fim - df_inicio) / df_inicio) * 100
    df_combined = df_combined.round(4)
    df_combined.to_sql(name='Data_Gold', con=engine, if_exists='append', index=False)
        
    print('Fim dos dados transformados')

  
    t_end = time()
    print('operaçao gold levou %.3f segundos' % (t_end - t_start))
    print('fim dos dados trasformados')
   