# Tech Challenge – Fase 04 | Data Analytics (Pos Tech)

## 1) Descrição do Projeto
Este projeto é a entrega do **Tech Challenge – Fase 04** da pós-graduação **Data Analytics (Pos Tech)**.

O objetivo é desenvolver uma solução completa de **Machine Learning aplicada à saúde**, capaz de estimar a **tendência à obesidade** a partir de variáveis de hábitos e contexto, apoiando análise e tomada de decisão.

Além do modelo, o projeto inclui:
- **App preditivo em Streamlit**
- **Dashboard analítico em Power BI**
- **Pipeline reprodutível** (EDA → Feature Engineering → Treino → Avaliação → Salvamento do modelo)

---

## 2) Objetivos (requisitos do desafio)
- Realizar **EDA (análise exploratória)**
- Preparar dados e realizar **feature engineering**
- Treinar e avaliar modelos (meta: **acurácia > 75%**)
- Persistir o modelo treinado (`.joblib`)
- Publicar um **app em Streamlit** (deploy)
- Construir um **dashboard** com insights (visão de negócio)
- Disponibilizar o projeto no GitHub

---

## 3) Base de Dados
Dataset: **Obesity.csv** (fornecido no desafio).

Durante o desenvolvimento, a base passou por:
- Tratamento inicial em **KNIME**
- Carga em **PostgreSQL**
- Consumo no **Power BI** para construção do dashboard
- Exportação de versões processadas para reprodução local (sem depender do banco)

Arquivos no projeto:
- `data/raw/Obesity.csv` (original)
- `data/processed/obesity_processed_postgres.csv` (processado para uso geral)
- `data/processed/obesity_processed_eda.csv` (saída após EDA)
- `data/features/obesidade_features.csv` (features consolidadas para treino, quando aplicável)

---

## 4) Variáveis Utilizadas (principais)
- Sexo, Idade
- Histórico familiar de sobrepeso
- Consumo de alimentos calóricos
- Ingestão de vegetais
- Número de refeições principais
- Comer entre refeições
- Tabagismo
- Consumo de água
- Monitoramento de calorias
- Frequência de atividade física
- Tempo de telas
- Consumo de álcool
- Meio de transporte

### Variável alvo
- `Obesity_level` (nível/classificação)

---

## 5) Decisão importante (evitar “IMC disfarçado”)
Para evitar que o modelo virasse apenas um cálculo determinístico de **IMC** (peso/altura²) e gerasse uma acurácia artificialmente alta por **vazamento de informação (data leakage)**, as features **peso** e **altura** foram **excluídas do treinamento**.

O foco do modelo é aprender padrões a partir de **hábitos e contexto**, e não reproduzir uma fórmula.

---

## 6) Pipeline de Machine Learning (notebooks)
O pipeline foi desenvolvido e documentado em dois notebooks:

- `notebooks/01_eda.ipynb`
  - análise de qualidade e exploração
  - remoção de duplicados
  - geração da base pós-EDA (`data/processed/obesity_processed_eda.csv`)

- `notebooks/02_feature_engineering.ipynb`
  - engenharia de features e recodificações
  - definição do target binário (`target_obeso`: obeso=1 / não obeso=0)
  - split treino/teste com estratificação
  - treino e comparação de modelos
  - avaliação (accuracy, matriz de confusão, ROC/AUC)
  - salvamento do artefato final `.joblib` (com `model`, `feature_columns`, `threshold`)

Modelo final utilizado no app:
- `models/modelo_rf.joblib` (**RandomForestClassifier**)

> Detalhes completos estão em: `notebooks/README.md`

---

## 7) Aplicação (Streamlit)
O modelo treinado é consumido por um app Streamlit:

- `app/app_obesidade.py`

O app:
1. coleta as respostas do usuário (formulário)
2. converte para valores numéricos (mapas)
3. monta uma linha (`X_novo`) com a ordem correta (`feature_columns`)
4. calcula probabilidade (`predict_proba`)
5. classifica com base em `threshold`

> Detalhes completos estão em: `app/README.md`

---

## 8) Dashboard (Power BI)
O dashboard está em:

- `dashboard/Obesidade.pbix`

Ele apresenta insights como:
- distribuição de classes / perfis
- relação entre hábitos e obesidade
- indicadores úteis para análise e prevenção

> Detalhes completos estão em: `dashboard/README.md`

---

## 9) Estrutura do Repositório
FASE4/
├── app/
│ ├── app_obesidade.py
│ └── README.md
├── dashboard/
│ ├── Obesidade.pbix
│ └── README.md
├── data/
│ ├── raw/
│ ├── processed/
│ ├── features/
│ └── README.md
├── models/
│ ├── modelo_rf.joblib
│ └── README.md
├── notebooks/
│ ├── 01_eda.ipynb
│ ├── 02_feature_engineering.ipynb
│ └── README.md
├── .gitignore
├── requirements.txt
└── README.md


---

## 10) Como executar (Windows / PowerShell)

### 1) Criar e ativar ambiente virtual
```powershell
cd C:\projetos\fase4
py -3.11 -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt

11) Links da entrega 
App Streamlit: [https://tc-fase4-obesidade-eduardo-gil-tivanello.streamlit.app/]

Dashboard Power BI (link publicado): [https://app.powerbi.com/view?r=eyJrIjoiMzQ4NjU1MjAtY2YwNi00NGZhLWI3NjEtYjQ1NjYxMzE2ZjNkIiwidCI6IjhhZjNmN2Y1LTUzYTQtNDcxYS1hMWI1LWI2N2E5YzQ4YTI1NCJ9]

Repositório GitHub: [https://github.com/tivanello/fase4]

Vídeo (4–10 min): [COLE AQUI]