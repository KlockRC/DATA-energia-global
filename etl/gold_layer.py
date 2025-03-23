import pandas as pd # type: ignore
from time import time

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


def trasformacao_insercao_dados_gold(engine):
    t_start = time()
    df_gold = pd.read_sql_table('Silver_Data', con=engine)
    for col in columns_to_fill:
        media_renovavel_por_pais = df_gold.groupby(["Country"])[col].mean().reset_index()
        media_renovavel_por_pais.to_csv(f"SRC/DATA/GOLD/media_{col}_por_pais.csv", index=False)
        media_renovavel_por_pais.to_sql(name=f'media_{col}_por_pais_Gold', con=engine, if_exists='append')

    for col in columns_to_fill:
        df_inicio = df_gold.groupby("Country").first().reset_index()
        df_fim = df_gold.groupby("Country").last().reset_index()

        df_crescimento = df_inicio[["Country", col]].merge(
            df_fim[["Country", col]], on="Country", suffixes=("-inicio", "-fim")
        )

        df_crescimento["Crescimento (%)"] = ((df_crescimento[f"{col}-fim"] - df_crescimento[f"{col}-inicio"]) / df_crescimento[f"{col}-inicio"]) * 100
        df_crescimento = df_crescimento.sort_values("Crescimento (%)", ascending=False)
        df_crescimento.to_csv(f"SRC/DATA/GOLD/crescimento_{col}_Gold.csv", index=False)
        df_crescimento.to_sql(name=f'crescimento_{col}_Gold', con=engine, if_exists='append')
        
        df_combined = pd.DataFrame()
    for col in columns_to_fill:
        media_renovavel_por_pais = df_gold.groupby("Country")[col].mean().reset_index()
        media_renovavel_por_pais.columns = media_renovavel_por_pais.columns.str.strip()
        media_renovavel_por_pais = media_renovavel_por_pais.rename(columns={col: f"media_{col}"})

        if df_combined.empty:
            df_combined = media_renovavel_por_pais
        else:
            df_combined = df_combined.merge(media_renovavel_por_pais, on="Country", how="outer")

        # Crescimento por país
        df_inicio = df_gold.groupby("Country").first().reset_index()
        df_fim = df_gold.groupby("Country").last().reset_index()

        df_crescimento = df_inicio[["Country", col]].merge(
            df_fim[["Country", col]], on="Country", suffixes=("-inicio", "-fim")
        )
        df_crescimento["Crescimento (%)"] = ((df_crescimento[f"{col}-fim"] - df_crescimento[f"{col}-inicio"]) / df_crescimento[f"{col}-inicio"]) * 100
        df_crescimento = df_crescimento.sort_values("Crescimento (%)", ascending=False)

        if "Crescimento (%)" in df_combined.columns:
            df_combined.rename(columns={"Crescimento (%)": f"Crescimento (%)_{col}"}, inplace=True)

        df_combined = df_combined.merge(df_crescimento[["Country", "Crescimento (%)"]], on="Country", how="outer")
    df_combined.to_csv('SRC/DATA/GOLD/tabela_combinada.csv', index=False)
    df_combined.to_sql(name='tabela_combinada_Gold', con=engine, if_exists='append', index=False)
    print('Fim dos dados transformados')

  

    t_end = time()
    print('operaçao gold levou %.3f segundos' % (t_end - t_start))
    print('fim dos dados trasformados')