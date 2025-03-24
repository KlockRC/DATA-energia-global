# ETL Pipeline com Airflow, Docker e AWS

Este projeto implementa uma pipeline de ETL (Extração, Transformação e Carga) utilizando o **Apache Airflow** para orquestrar as tarefas, **Docker** para containerização, e **AWS S3** para armazenamento de dados. A pipeline realiza a coleta de dados, limpeza, transformação e armazenamento em um banco de dados PostgreSQL.

## Arquitetura

A arquitetura é composta por três camadas principais:
1. **Bronze Layer**: Extração dos dados a partir de um arquivo CSV armazenado no S3.
2. **Silver Layer**: Limpeza e transformação dos dados.
3. **Gold Layer**: Geração de agregações e análises dos dados.

O pipeline é orquestrado utilizando o **Apache Airflow**, que é executado dentro de um container Docker, e os dados são armazenados em um banco de dados **PostgreSQL** em um ambiente local ou em cloud.

### Diagrama de fluxo da pipeline:

Inicio -> Bronze Layer -> Silver Layer -> Gold Layer -> Fim

**Há como execultar o projeto sem  o airflow ou docker usando o (pipeline_demonstrativa.py)**

Pré-requisitos
Antes de rodar o projeto, é necessário ter os seguintes pré-requisitos instalados:

1. Docker: Para containerizar a aplicação.
2. Docker Compose: Para facilitar a criação e orquestração de containers.
3. AWS S3: Para armazenar os dados CSV. (arquivo csv dento de /SRC/DATA)

**Criar a imagem Docker personalizada para o Airflow**

Para rodar o Airflow, você precisará construir uma imagem Docker personalizada. No diretório do projeto. **(Arquivo Dockerfile já disponivel)**

```
docker build -t Airflow_Mod .
```


**Variáveis de ambiente**

Configure o arquivo **variaveis.env** com os dados do DB e o arquivo CSV

**Iniciar os containers**

Com o Docker e o Docker Compose configurados, inicie os containers com:
Primeiro com:

```
docker-compose up -d airflow-init
```

Logo após com:
```
docker-compose up -d
```

Isso iniciará os containers para o Airflow, PostgreSQL e qualquer outro serviço necessário.

**Acessar o Airflow**
Depois de iniciar os containers, você pode acessar a interface web do Airflow em:
```
http://localhost:8080
```
Faça login com 
usuario:**admin** senha:**admin** 
e ative o DAG etl_pipeline para começar a execução das tarefas.

**Como funciona**

A pipeline é dividida em três tarefas principais, cada uma representada por uma camada:

1. Bronze Layer:
A Bronze Layer é responsável pela extração dos dados do arquivo CSV armazenado no AWS S3 e inserção no banco de dados PostgreSQL.

Função: bronze_inserir_no_db()

2. Silver Layer:
Na Silver Layer, os dados são limpos e transformados. Dados faltantes são preenchidos com a mediana, e os valores são ajustados conforme necessário.

Função: silver_limpesa_insercao_dados_silver()

3. Gold Layer:
A Gold Layer realiza as agregações e análises dos dados. Calcula-se a média por país para cada coluna e o crescimento percentual entre o início e o fim do período de dados.

Função: gold_trasformacao_insercao_dados_gold()

As tarefas são interdependentes, com a execução do DAG começando na tarefa "Inicio" e passando pela camada Bronze, Silver e Gold até a conclusão.

**Este projeto é uma implementação simples e eficiente de um pipeline ETL utilizando Apache Airflow, Docker e PostgreSQL. Ele pode ser facilmente escalado e adaptado para outros casos de uso.**