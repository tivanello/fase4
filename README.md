Tech Challenge – Fase 04 | Data Analytics (Pos Tech)
1. Descrição do Projeto

Este projeto integra o Tech Challenge – Fase 04 da pós-graduação Data Analytics (Pos Tech) e tem como objetivo o desenvolvimento de uma solução completa de Machine Learning aplicada à área da saúde.

O desafio consiste em construir um modelo preditivo capaz de estimar o nível de obesidade de uma pessoa, com o propósito de auxiliar médicos e médicas no apoio à decisão clínica.

A obesidade é uma condição multifatorial, influenciada por aspectos genéticos, comportamentais e ambientais. A partir de dados estruturados, este projeto busca identificar padrões relevantes e gerar previsões com desempenho adequado para uso analítico e preditivo.

2. Objetivo do Projeto

Desenvolver uma pipeline completa de Machine Learning, contemplando todas as etapas exigidas no Tech Challenge:

Análise exploratória e compreensão do problema de negócio

Tratamento e preparação dos dados

Feature engineering

Treinamento e avaliação de modelos preditivos

Modelo com acurácia superior a 75%

Deploy do modelo em uma aplicação Streamlit

Construção de um painel analítico com insights relevantes sobre obesidade

Disponibilização do código-fonte no GitHub

3. Base de Dados

O projeto utiliza o dataset obesity.csv, fornecido no enunciado do desafio.

Durante o desenvolvimento, os dados também foram tratados no KNIME e disponibilizados no PostgreSQL, permitindo:

padronização do processo de preparação

integração com Power BI para o painel analítico

exportação de uma base “processada” para reprodução local sem dependência de banco

4. Variáveis Utilizadas

Gender: Gênero

Age: Idade

Height: Altura (m)

Weight: Peso (kg)

family_history: Histórico familiar de excesso de peso

FAVC: Consumo frequente de alimentos calóricos

FCVC: Frequência de consumo de vegetais

NCP: Número de refeições principais diárias

CAEC: Consumo de alimentos entre as refeições

SMOKE: Hábito de fumar

CH2O: Consumo diário de água

SCC: Monitoramento da ingestão calórica

FAF: Frequência de atividade física

TUE: Tempo de uso de dispositivos eletrônicos

CALC: Consumo de bebida alcoólica

MTRANS: Meio de transporte utilizado

5. **Variável Alvo**

Obesity_level: Classificação do nível de obesidade

6. Pipeline de Machine Learning

A solução foi estruturada seguindo boas práticas de Data Analytics, Deploy de Aplicações e Machine Learning em Produção, contemplando:

Análise exploratória dos dados (EDA)

Tratamento de variáveis categóricas e numéricas

Feature engineering

Treinamento e validação de modelos

Avaliação de desempenho (acurácia > 75%)

Persistência do modelo treinado

Preparação do modelo para uso em produção

7. Deploy da Aplicação

O modelo treinado é disponibilizado por meio de uma aplicação preditiva desenvolvida em Streamlit, permitindo que profissionais de saúde insiram dados e obtenham previsões de forma simples e direta.

Adicionalmente, foi construído um painel analítico com os principais insights obtidos a partir dos dados, apresentado em uma visão orientada ao negócio, com foco no apoio à equipe médica.

8. Painel Analítico

O painel apresenta, entre outros pontos:

Distribuição dos níveis de obesidade

Relação entre hábitos de vida e obesidade

Perfis de maior risco

Indicadores relevantes para prevenção e acompanhamento clínico

9. Estrutura do Repositório
fase4/
│
├── data/
│   ├── raw/               # Dados brutos (dataset original)
│   └── processed/         # Dados tratados (pronto para treino/reprodução)
│
├── notebooks/
│   ├── 01_eda.ipynb
│   └── 02_feature_engineering.ipynb
│
├── src/
│   ├── data.py
│   ├── export_processed.py
│   ├── preprocessing.py
│   ├── features.py
│   ├── train.py
│   └── evaluate.py
│
├── app/
│   └── streamlit_app.py
│
├── dashboard/             # Painel analítico (Power BI)
│
├── README.md
└── requirements.txt

## **Como executar o projeto (Windows/PowerShell)**
1) Criar e ativar ambiente virtual
cd C:\projetos\fase4
py -3.11 -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt

2) Configurar o .env

Crie um arquivo .env na raiz do projeto.

Opção A — Rodar via CSV processado (recomendado para reprodução fácil)
DATA_SOURCE=processed_csv


O arquivo esperado é:

data/processed/obesity_processed_postgres.csv

Opção B — Rodar via PostgreSQL
DATA_SOURCE=postgres
DB_HOST=localhost
DB_PORT=5432
DB_NAME=tech_challenge_fase4
DB_USER=SEU_USUARIO
DB_PASS=SUA_SENHA
DB_SCHEMA=public
DB_TABLE=obesidade

3) (Opcional) Exportar do PostgreSQL para data/processed/

Gera o arquivo:

data/processed/obesity_processed_postgres.csv

python -m src.export_processed

4) Treinar o modelo
python -m src.train


Artefatos gerados:

models/model.joblib

models/meta.json

5) Avaliar o modelo
python -m src.evaluate

6) Executar o Streamlit (Deploy)
streamlit run app/streamlit_app.py

**Observações importantes**

O arquivo requirements.txt deve conter somente dependências Python.
Configurações como DATA_SOURCE=... devem ficar no .env.

Recomenda-se incluir um .env.example no repositório e adicionar .env ao .gitignore para evitar exposição de senha.