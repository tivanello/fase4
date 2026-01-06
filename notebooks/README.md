# Notebooks – Pipeline de Machine Learning (Obesidade)

Este diretório contém os notebooks usados para construir o pipeline de ML do projeto (EDA + feature engineering + treino, avaliação e salvamento do modelo).

---

## Ponto crítico do projeto (muito importante)
Para evitar que o problema virasse apenas um **cálculo determinístico de IMC** (regra) e não um modelo de **Machine Learning**, as features **`peso`** e **`altura`** foram **removidas do conjunto de treino**.

**Motivo:**
- Com `peso` e `altura`, o modelo aprende quase diretamente o IMC (peso / altura²).
- Isso geraria **vazamento de informação (data leakage)** e inflaria a acurácia de forma artificial.
- O objetivo aqui é prever **tendência/risco** com base em **hábitos e contexto**, não reproduzir uma fórmula.

Assim, o modelo foi treinado usando principalmente variáveis de **hábitos e estilo de vida**, como histórico familiar, consumo alimentar, atividade física, consumo de água, álcool, telas, transporte etc.

---

## 01_eda.ipynb — Análise Exploratória (EDA)

**Objetivo:** entender a base, checar qualidade dos dados e gerar uma versão “pós-EDA” pronta para a etapa de modelagem.

**O que foi feito:**
- Leitura do dataset processado (após tratamento inicial feito fora do notebook).
- Verificação de estrutura do dataset:
  - dimensões, tipos das colunas e amostra (`head()`).
- Análise de qualidade:
  - identificação e remoção de registros duplicados.
  - checagem de valores ausentes (quando aplicável).
- Exploração de variáveis:
  - estatísticas descritivas (numéricas).
  - contagens e distribuição (categóricas).
  - análise por classe (relação de variáveis com o alvo).
- Exportação do dataset pós-EDA para:
  - `../data/processed/obesity_processed_eda.csv`

**Saída deste notebook:**
- Arquivo `obesity_processed_eda.csv` (base preparada para feature engineering e treino).

---

## 02_feature_engineering.ipynb — Engenharia de Features + Treino e Avaliação

**Objetivo:** transformar variáveis para ML, definir o alvo, treinar modelos, avaliar performance e salvar o modelo final para uso no app Streamlit.

**O que foi feito:**

### 1) Leitura da base pós-EDA
- Carregamento de `../data/processed/obesity_processed_eda.csv`

### 2) Preparação do dataset para ML (sem “IMC disfarçado”)
- Remoção explícita das features **`peso`** e **`altura`** do conjunto de treino, para evitar que o modelo apenas reproduzisse o cálculo do IMC.

### 3) Feature Engineering (transformações)
- Padronização/recodificação de variáveis categóricas e ajustes de rótulos.
- Criação/recodificação do target para classificação binária:
  - `target_obeso` (Obeso = 1 / Não obeso = 0), a partir de `Obesity_level`.

### 4) Preparação para modelagem
- Separação entre `X` (features) e `y` (target).
- Split treino/teste com estratificação:
  - `train_test_split(..., stratify=y, test_size=0.2, random_state=42)`

### 5) Treinamento e comparação de modelos
- Treino e avaliação de múltiplos classificadores (exemplos):
  - Logistic Regression, Random Forest, Extra Trees, Gradient Boosting, HistGradientBoosting, SVC.
- Métricas geradas:
  - Acurácia (accuracy)
  - Relatório de classificação (precision/recall/f1)
  - Matriz de confusão (incluindo versão normalizada)
  - Curva ROC e AUC

### 6) Seleção do modelo final e salvamento
- Seleção do modelo com melhor desempenho.
- Definição de um threshold para converter probabilidade em classe (0/1).
- Salvamento do artefato `.joblib`, incluindo:
  - objeto `model`
  - `threshold`
  - `
