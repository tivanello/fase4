# Data (bases do projeto)

Este diretório organiza as bases utilizadas no projeto em três etapas: **raw → processed → features**.

A ideia é manter rastreabilidade: de onde o dado veio, como foi tratado e o que foi usado no modelo.

---

## Estrutura

### 1) `raw/`
**Conteúdo bruto (sem transformação para ML).**

- `Obesity.csv`  
  Dataset original recebido para o projeto.  
  É a “fonte” a partir da qual todo o restante é gerado.

---

### 2) `processed/`
**Bases já tratadas e prontas para análise/modelagem.**

- `obesity_processed_postgres.csv`  
  Versão processada após tratamento inicial (ex.: ajustes no KNIME) e usada como base para carga no PostgreSQL e consumo no Power BI/Jupyter.

- `obesity_processed_eda.csv`  
  Versão gerada após a etapa de EDA (ex.: remoção de duplicados e ajustes necessários), usada como entrada no notebook de feature engineering e treinamento do modelo.

---

### 3) `features/`
**Base final de features usada diretamente no modelo.**

- `obesidade_features.csv`  
  Dataset consolidado após engenharia de features:
  - variáveis recodificadas
  - encodings aplicados (quando necessário)
  - target preparado para treino
  - pronto para `train_test_split` e modelagem

---

## Observação importante (para evitar “IMC disfarçado”)
Para manter o problema como **Machine Learning de tendência/risco** e não um simples cálculo de IMC, as colunas **`peso`** e **`altura`** foram removidas do conjunto de treino na etapa de modelagem.

---

## Fluxo resumido de uso
`raw/Obesity.csv`  
→ tratamento inicial (KNIME / carga Postgres)  
→ `processed/obesity_processed_postgres.csv`  
→ EDA  
→ `processed/obesity_processed_eda.csv`  
→ feature engineering  
→ `features/obesidade_features.csv`  
→ treino e salvamento do modelo (`models/`)
