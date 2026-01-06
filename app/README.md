# App Streamlit – Questionário de Tendência à Obesidade

Este app foi desenvolvido em **Streamlit** para consumir o modelo treinado (salvo em `.joblib`) e retornar:

- Classificação: **Obeso** / **Não obeso**
- Probabilidade estimada (%)
- Threshold utilizado na decisão

---

## Como funciona (resumo)
1. O usuário preenche um formulário com variáveis de **hábitos e estilo de vida**.
2. O app transforma as respostas em valores numéricos usando mapas (ex.: "Sim/Não", frequência, transporte etc.).
3. Uma linha (`X_novo`) é montada como DataFrame.
4. O app garante a **ordem exata das colunas** usando `feature_columns` que vem dentro do `.joblib`.
5. O modelo calcula `predict_proba`.
6. A classificação final é feita usando um **threshold** (ex.: 0.41):
   - se `proba >= threshold` → **Obeso**
   - senão → **Não obeso**

---

## Arquivo do modelo utilizado
O app carrega o modelo em:

- `../models/modelo_rf.joblib`

Este `.joblib` é um **dicionário** contendo, entre outros:
- `model` (modelo treinado)
- `feature_columns` (colunas/ordem esperada pelo modelo)
- `threshold` (limiar usado na decisão)

---

## Observação importante (evitar “IMC disfarçado”)
As colunas **peso** e **altura** não são usadas no app/modelo para evitar que a classificação vire apenas um cálculo determinístico de IMC.
O objetivo aqui é estimar tendência/risco com base em hábitos e contexto.

---

## Como executar localmente
A partir da raiz do projeto:

```bash
pip install -r requirements.txt
streamlit run app/app_obesidade.py
