from sqlalchemy import create_engine  # type: ignore
from etl import bronze_layer as bronze
from etl import silver_layer as silver
from etl import gold_layer as gold


endpoint = 'postgresql://root:GlobE@localhost:5433/energia_glob'

engine = create_engine(endpoint)

print('iniciando camada bronze')
 
bronze.bronze_inserir_no_db(engine)

print('iniciando camada silver')

silver.limpesa_insercao_dados_silver(engine)

print('iniciando camada gold')

gold.trasformacao_insercao_dados_gold(engine)


