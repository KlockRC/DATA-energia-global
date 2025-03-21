import pandas as pd
from sqlalchemy import create_engine
from time import time

engine = create_engine('postgresql://root:GlobE@localhost:5433/energia_glob')
df_gold = pd.read_csv('SRC/DATA/Silver.csv')

media_renovavel_por_pais = df_gold.groupby(["Country"])["Renewable Energy Share (%)"].mean().reset_index()
comparacao_fossil_emissoes = df_gold.groupby("Country")[["Fossil Fuel Dependency (%)", "Carbon Emissions (Million Tons)"]].mean().reset_index()

df_inicio = df_gold.groupby("Country").first().reset_index()
df_fim = df_gold.groupby("Country").last().reset_index()

df_crescimento = df_inicio[["Country", "Per Capita Energy Use (kWh)"]].merge(
    df_fim[["Country", "Per Capita Energy Use (kWh)"]], on="Country", suffixes=("inicio", "fim")
)

df_crescimento["Crescimento (%)"] = ((df_crescimento["Per Capita Energy Use (kWh)fim"] - df_crescimento["Per Capita Energy Use (kWh)inicio"]) / df_crescimento["Per Capita Energy Use (kWh)inicio"]) * 100
df_crescimento = df_crescimento.sort_values("Crescimento (%)", ascending=False)
correlacao = df_gold[["Energy Price Index (USD/kWh)", "Fossil Fuel Dependency (%)"]].corr()


correlacao.to_csv("SRC/DATA/GOLD/correlacao_precos_fossil.csv")
df_crescimento.to_csv("SRC/DATA/GOLD/crescimento_energia_per_capita.csv", index=False)
comparacao_fossil_emissoes.to_csv("SRC/DATA/GOLD/comparacao_fossil_emissoes.csv", index=False)
media_renovavel_por_pais.to_csv("SRC/DATA/GOLD/media_renovavel_por_pais.csv", index=False)

correlacao.to_sql(name='Correlacao_Gold', con=engine, if_exists='append')
df_crescimento.to_sql(name='crescimento_Gold', con=engine, if_exists='append')
comparacao_fossil_emissoes.to_sql(name='comparacao_fossil_emissoes_Gold', con=engine, if_exists='append')
media_renovavel_por_pais.to_sql(name='media_renovavel_por_pais_Gold', con=engine, if_exists='append')