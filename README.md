# ETL Pipeline com Airflow, Docker e AWS

Este projeto implementa uma pipeline de ETL (Extração, Transformação e Carga) utilizando o **Apache Airflow** para orquestrar as tarefas, **Docker** para containerização, e **AWS S3** para armazenamento de dados. A pipeline realiza a coleta de dados, limpeza, transformação e armazenamento em um banco de dados PostgreSQL.

## Arquitetura

A arquitetura é composta por três camadas principais:
1. **Bronze Layer**: Extração dos dados a partir de um arquivo CSV armazenado no S3.
2. **Silver Layer**: Limpeza e transformação dos dados.
3. **Gold Layer**: Geração de agregações e análises dos dados.

O pipeline é orquestrado utilizando o **Apache Airflow**, que é executado dentro de um container Docker, e os dados são armazenados em um banco de dados **PostgreSQL**, também gerenciado através do Docker. 

### Diagrama de fluxo da pipeline:

```plaintext
Inicio -> Bronze Layer -> Silver Layer -> Gold Layer -> Fim
Pré-requisitos
Antes de rodar o projeto, é necessário ter os seguintes pré-requisitos instalados:

Docker: Para containerizar a aplicação.

Docker Compose: Para facilitar a criação e orquestração de containers.

Apache Airflow: Para orquestrar as tarefas da pipeline.

AWS S3: Para armazenar os dados CSV.

PostgreSQL: Para armazenamento dos dados processados.

Setup
1. Criar a imagem Docker personalizada para o Airflow
Para rodar o Airflow, você precisará construir uma imagem Docker personalizada. No diretório do projeto, execute:

bash
Copiar
Editar
docker build -t airflow-custom .
2. Variáveis de ambiente
O arquivo docker-compose.yml deve ser configurado com as seguintes variáveis de ambiente para o PostgreSQL e AWS:

yaml
Copiar
Editar
environment:
  POSTGRES_USER: your_user
  POSTGRES_PASSWORD: your_password
  POSTGRES_HOST: db
  POSTGRES_PORT: 5432
  POSTGRES_DB: your_database
  CSV_S3: s3://your-bucket/your-csv-file.csv
3. Iniciar os containers
Com o Docker e o Docker Compose configurados, inicie os containers com:

bash
Copiar
Editar
docker-compose up -d
Isso iniciará os containers para o Airflow, PostgreSQL e qualquer outro serviço necessário.

4. Acessar o Airflow
Depois de iniciar os containers, você pode acessar a interface web do Airflow em:

plaintext
Copiar
Editar
http://localhost:8080
Faça login e ative o DAG etl_pipeline para começar a execução das tarefas.

Como funciona
A pipeline é dividida em três tarefas principais, cada uma representada por uma camada:

1. Bronze Layer:
A Bronze Layer é responsável pela extração dos dados do arquivo CSV armazenado no AWS S3 e inserção no banco de dados PostgreSQL.

Função: bronze_inserir_no_db()

2. Silver Layer:
Na Silver Layer, os dados são limpos e transformados. Dados faltantes são preenchidos com a mediana por país, e os valores são ajustados conforme necessário.

Função: silver_limpesa_insercao_dados_silver()

3. Gold Layer:
A Gold Layer realiza as agregações e análises dos dados. Calcula-se a média por país para cada coluna e o crescimento percentual entre o início e o fim do período de dados.

Função: gold_trasformacao_insercao_dados_gold()

Dockerfile
O Dockerfile utilizado para a criação da imagem personalizada para o Airflow é o seguinte:

Dockerfile
Copiar
Editar
FROM apache/airflow:2.5.0

USER root

# Instalar dependências adicionais
RUN apt-get update && apt-get install -y \
    python3-pandas \
    python3-sqlalchemy \
    && rm -rf /var/lib/apt/lists/*

# Instalar pacotes necessários
COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt

USER airflow
Como construir a imagem Docker:
bash
Copiar
Editar
docker build -t airflow-custom .
Executando a Pipeline
O DAG etl_pipeline é executado diariamente (schedule_interval="@daily").

O DAG consiste nas seguintes tarefas:

Inicio: Início da execução.

Bronze Layer: Extração e inserção no banco de dados.

Silver Layer: Limpeza e transformação dos dados.

Gold Layer: Cálculo de médias e crescimento.

Fim: Fim da execução.

As tarefas são interdependentes, com a execução do DAG começando na tarefa "Inicio" e passando pela camada Bronze, Silver e Gold até a conclusão.

Conclusão
Este projeto é uma implementação simples e eficiente de um pipeline ETL utilizando Apache Airflow, Docker e PostgreSQL. Ele pode ser facilmente escalado e adaptado para outros casos de uso.