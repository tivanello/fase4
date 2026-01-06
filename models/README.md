# Models (artefatos .joblib)

Este diretório armazena o modelo final treinado para a aplicação Streamlit.

## Modelo utilizado

O modelo final salvo neste diretório é um **Random Forest** do scikit-learn, classe:
- `RandomForestClassifier`

Esse objeto já está **treinado (fit)** e é carregado pelo app Streamlit para gerar `predict_proba` e a classificação final usando o `threshold`.

---


## modelo_rf.joblib

Arquivo do tipo **dicionário (dict)** salvo com `joblib`, contendo os seguintes campos:

- `model` : objeto do modelo treinado (scikit-learn)
- `feature_columns` : lista **na ordem correta** das colunas usadas no treino (referência para montar o `X` no app)
- `labels` : rótulos/classes usados no treinamento (mapeamento da saída)
- `acc` : acurácia do modelo no conjunto de teste (referência)
- `auc_macro` : AUC macro (quando aplicável)
- `params` : parâmetros do modelo (para rastreabilidade)
- `threshold` : limiar usado para converter probabilidade em classe (ex.: `proba >= threshold` → 1)

---

## Como o app usa este arquivo
O `app/app_obesidade.py` carrega o `.joblib`, recupera:
- `model` para `predict_proba`
- `threshold` para a decisão final (obeso / não obeso)
- `feature_columns` para garantir compatibilidade e ordem das features
