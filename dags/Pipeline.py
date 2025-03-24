from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator, PythonVirtualenvOperator
from datetime import datetime
import pandas as pd
from etl import etl

default_args = {
    "owner": "Cesar",
    "start_date": datetime(2025, 3, 23),
    "retries": 1,
    "log_level": "DEBUG",
}

dag = DAG(
    "etl_pipeline",
    default_args=default_args,
    schedule_interval="@daily",
    catchup=False,
)

Inicio = EmptyOperator(
    task_id="inicio",
    dag=dag
)

task_bronze = PythonOperator(
    task_id="bronze_layer",
    #requirements=["sqlalchemy<2.0,>=1.4.36", "pandas==2.2.3", "panda==0.3.1"],
    python_callable=etl.bronze_inserir_no_db,
    #op_kwargs={'pd': pd},
    #system_site_packages=False,
    dag=dag
)

task_silver = PythonOperator(
    task_id="silver_layer",
    #requirements=["sqlalchemy<2.0,>=1.4.36", "pandas==2.2.3", "panda==0.3.1"],
    python_callable=etl.silver_limpesa_insercao_dados_silver,
    #system_site_packages=False,
    dag=dag
)

task_gold = PythonOperator(
    task_id="gold_layer",
    #requirements=["sqlalchemy<2.0,>=1.4.36", "pandas==2.2.3", "panda==0.3.1"],
    python_callable=etl.gold_trasformacao_insercao_dados_gold,
    #system_site_packages=False,
    dag=dag
)

Fim = EmptyOperator(
    task_id="Fim",
    dag=dag
)

Inicio >> task_bronze >> task_silver >> task_gold >> Fim