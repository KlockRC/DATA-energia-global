from sqlalchemy import create_engine  # type: ignore
from etl import bronze_layer as bronze
from etl import silver_layer as silver
from etl import gold_layer as gold

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

endpoint = 'postgresql://root:GlobE@localhost:5433/energia_glob'

engine = create_engine(endpoint)

print('iniciando camada bronze')
 
bronze.bronze_inserir_no_db(engine)

print('iniciando camada silver')

silver.limpesa_insercao_dados_silver(engine, columns_to_fill, replace_dict, collumns_to_check)

print('iniciando camada gold')

gold.trasformacao_insercao_dados_gold(engine, columns_to_fill)

#comentario legal
