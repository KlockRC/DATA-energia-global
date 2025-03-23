import pandas as pd # type: ignore
from time import time


def trasformacao_insercao_dados_gold(engine, columns_to_fill ):
    t_start = time()
    df_gold = pd.read_sql_table('Silver_Data', con=engine)
    for col in columns_to_fill:
        media_unica_por_pais = df_gold.groupby(["Country"])[col].mean().reset_index()
        media_unica_por_pais = media_unica_por_pais.round(4)
        media_unica_por_pais.to_csv(f"SRC/DATA/GOLD/media_{col}_por_pais.csv", index=False)
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
        df_crescimento.to_csv(f"SRC/DATA/GOLD/crescimento_{col}_Gold.csv", index=False)
        df_crescimento.to_sql(name=f'crescimento_{col}_Gold', con=engine, if_exists='append')


#---------------------------------------------------------------------------------------------------------------------------------------#
    df_combined = pd.DataFrame(index=df_gold["Country"].unique())
    for col in columns_to_fill:
        media_por_pais = df_gold.groupby("Country")[col].mean()
        df_combined[f"media_{col}"] = media_por_pais
        df_inicio = df_gold.groupby("Country", as_index=True).first()[col]
        df_fim = df_gold.groupby("Country", as_index=True).last()[col]
        
        df_combined[f"Crescimento (%)_{col}"] = ((df_fim - df_inicio) / df_inicio) * 100
    df_combined = df_combined.round(4)
    df_combined.to_csv('SRC/DATA/GOLD/Gold.csv', index=False)
    df_combined.to_sql(name='Data_Gold', con=engine, if_exists='append', index=False)
        
    print('Fim dos dados transformados')

  
    t_end = time()
    print('operaçao gold levou %.3f segundos' % (t_end - t_start))
    print('fim dos dados trasformados')