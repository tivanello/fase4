# app_obesidade.py
import streamlit as st
import pandas as pd
import numpy as np
import joblib


# Configuração
#======================

st.set_page_config(page_title="App Obesidade", page_icon="🍽️", layout="centered")

# MODEL_PATH = r"C:\projetos\fase4\models\modelo_rf.joblib" # Executa local

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]   # volta pra raiz do projeto
MODEL_PATH = BASE_DIR / "models" / "modelo_rf.joblib"


st.markdown(
    "<style>div[role='listbox'] ul{background-color: #6e42ad};</style>",
    unsafe_allow_html=True
)

st.markdown(
    "<h1 style='text-align: center;'>Questionário de Tendência à Obesidade 🍽️</h1>",
    unsafe_allow_html=True
)

st.markdown("""
<div style="
    background-color: rgba(33,150,243,0.15);
    border-left: 6px solid rgba(33,150,243,1);
    padding: 12px 16px;
    border-radius: 6px;
    text-align: center;
">
    Preencha os campos e clique em <b>Avaliar</b>.<br>
    O modelo retorna a sua <b>Probabilidade</b> e <b>Tendência</b> para obesidade.
</div>
""", unsafe_allow_html=True)



# CARREGAMENTO DO MODELO (artefato)
# =======================

@st.cache_resource
def carregar_artefato(caminho: str):
    artefato = joblib.load(caminho)

    # Segurança: Se não for um dicionário (dict) será interrompido e apresentará erro.

    if not isinstance(artefato, dict):
        raise TypeError("O arquivo .joblib não é um dicionário (artefato).")

    model = artefato["model"]
    feature_columns = artefato.get("feature_columns")
    threshold = float(artefato.get("threshold", 0.5))

    return artefato, model, feature_columns, threshold

try:
    artefato, model, feature_columns, threshold = carregar_artefato(MODEL_PATH)
except Exception as e:
    st.error(f"Erro ao carregar o modelo em: {MODEL_PATH}\n\n{e}")
    st.stop()


# MAPAS PARA UI (INTERFACE DO USUÁRIO)
# ========================================

MAPA_SEXO_UI = {"Feminino": 0, "Masculino": 1}
MAPA_SIM_NAO_UI = {"Não": 0, "Sim": 1}
MAPA_FREQUENCIA_0_3_UI = {"Nunca": 0, "Às vezes": 1, "Frequentemente": 2, "Sempre": 3}
MAPA_TEMPO_TELA_0_2_UI = {"Menos de 1 hora por dia": 0, "de 1 a 3 horas por dia": 1, "mais de 3 horas por dia": 2}
MAPA_TRANSPORTE_0_4_UI = {"Caminhando": 0, "Bicicleta": 1, "Transporte público": 2, "Automóvel": 3, "Moto": 4}
MAPA_NIVEL_1_3_VEGETAIS_UI = {"Pouco (quase não coloco no prato)": 1, "Normal (uma porção no prato)": 2, "Bastante (metade do prato ou mais)": 3}
MAPA_REFEICOES_UI = {"Apenas uma": 1, "Duas Refeições": 2, "Três Refeições": 3, "Quatro Refeições": 4, "Cinco Refeições": 5}
MAPA_ATIVIDADE_0_3_UI = {"Nenhuma": 0, "Uma Vez por semana": 1, "duas a três vezes por semana": 2, "Mais de três vezes por semana": 3}
MAPA_ALCOOL_0_3_UI = {"Não bebo": 0, "Às vezes (1)": 1, "Frequentemente (2)": 2, "Sempre (3)": 3}
MAPA_NIVEL_AGUA_1_3_UI = {"Apenas 1 litro por dia": 1, "Dois litros por dia": 2, "três litros o mais por dia": 3}



# FORMULÁRIO (entrada de dados)
# =======================
with st.form("form_obesidade"):
    st.write("## Dados básicos")

    col1, col2 = st.columns(2)
    with col1:
        sexo_txt = st.selectbox("Sexo", list(MAPA_SEXO_UI.keys()))
    with col2:
        idade = st.slider("Idade", 10, 100, 30)

    st.write("## Hábitos")

    col3, col4 = st.columns(2)
    with col3:
        historico_familiar_txt = st.radio("Histórico familiar de sobrepeso?", list(MAPA_SIM_NAO_UI.keys()), horizontal=True)
        ingere_alim_calorico_txt = st.radio("Costuma ingerir alimentos calóricos?", list(MAPA_SIM_NAO_UI.keys()), horizontal=True)
        fumante_txt = st.radio("Fumante?", list(MAPA_SIM_NAO_UI.keys()), horizontal=True)
        monitora_calorias_txt = st.radio("Monitora calorias?", list(MAPA_SIM_NAO_UI.keys()), horizontal=True)

    with col4:
        come_entre_refeicao_txt = st.selectbox("Come entre refeições?", list(MAPA_FREQUENCIA_0_3_UI.keys()))
        frequencia_consumo_alcool_txt = st.selectbox("Consumo de álcool", list(MAPA_ALCOOL_0_3_UI.keys()))
        meio_de_transporte_txt = st.selectbox("Meio de transporte principal", list(MAPA_TRANSPORTE_0_4_UI.keys()))

    st.write("## Quantidades / Frequências")

    col5, col6 = st.columns(2)
    with col5:
        ingere_vegetais_txt = st.selectbox("Ingestão de vegetais", list(MAPA_NIVEL_1_3_VEGETAIS_UI.keys()), index=1)
        qtd_refeicao_principal_txt = st.selectbox("Refeições principais por dia", list(MAPA_REFEICOES_UI.keys()), index=2)
        consumo_agua_litro_txt = st.selectbox("Consumo de água", list(MAPA_NIVEL_AGUA_1_3_UI.keys()), index=1)

    with col6:
        freq_atividade_fisica_txt = st.selectbox("Atividade física", list(MAPA_ATIVIDADE_0_3_UI.keys()), index=1)
        tempo_uso_eletronico_txt = st.selectbox("Tempo diário de telas", list(MAPA_TEMPO_TELA_0_2_UI.keys()), index=1)

    submit = st.form_submit_button("Avaliar")

# CÁLCULO DO RESULTADO / CLASSIFICAÇÃO (resultado do modelo)
# =======================
if submit:
    linha = {
        "sexo": MAPA_SEXO_UI[sexo_txt],
        "idade": float(idade),
        "historico_familiar": MAPA_SIM_NAO_UI[historico_familiar_txt],
        "ingere_alim_calorico": MAPA_SIM_NAO_UI[ingere_alim_calorico_txt],
        "ingere_vegetais": MAPA_NIVEL_1_3_VEGETAIS_UI[ingere_vegetais_txt],
        "qtd_refeicao_principal": MAPA_REFEICOES_UI[qtd_refeicao_principal_txt],
        "come_entre_refeicao": MAPA_FREQUENCIA_0_3_UI[come_entre_refeicao_txt],
        "fumante": MAPA_SIM_NAO_UI[fumante_txt],
        "consumo_agua_litro": MAPA_NIVEL_AGUA_1_3_UI[consumo_agua_litro_txt],
        "monitora_calorias": MAPA_SIM_NAO_UI[monitora_calorias_txt],
        "freq_atividade_fisica": MAPA_ATIVIDADE_0_3_UI[freq_atividade_fisica_txt],
        "tempo_uso_eletronico": MAPA_TEMPO_TELA_0_2_UI[tempo_uso_eletronico_txt],
        "frequencia_consumo_alcool": MAPA_ALCOOL_0_3_UI[frequencia_consumo_alcool_txt],
        "meio_de_transporte": MAPA_TRANSPORTE_0_4_UI[meio_de_transporte_txt],
    }

    X_novo = pd.DataFrame([linha])

    # Garante ordem exata das colunas
    if feature_columns is not None:
        faltando = [c for c in feature_columns if c not in X_novo.columns]
        if faltando:
            st.error(f"Faltam colunas exigidas pelo modelo: {faltando}")
            st.stop()
        X_novo = X_novo[feature_columns]
    else:
        # fallback: usa a lista COLS
        X_novo = X_novo[COLS]

    # Probabilidade e decisão por threshold
    if not hasattr(model, "predict_proba"):
        st.error("Seu modelo não possui predict_proba(). Para RandomForest, deveria ter. Verifique o artefato salvo.")
        st.stop()

    proba = float(model.predict_proba(X_novo)[:, 1][0])
    pred = 1 if proba >= threshold else 0    
  
    if pred == 1:
        st.error("### Classificação do modelo: **Obeso**")
        st.write(f"Pelas respostas informadas, o modelo estimou probabilidade ({int(round(proba*100))}%) de obesidade e classificou como **Obeso**.")
    else:
        st.success("### Classificação do modelo: **Não obeso**")
        st.write(f"Pelas respostas informadas, o modelo estimou baixa probabilidade ({int(round(proba*100))}%) de obesidade e classificou como **Não obeso**.")

    st.write("---")
    st.write("## Resultado")

    st.metric("Probabilidade estimada de obesidade", f"{int(round(proba*100))}%")
    st.caption(f"Threshold usado: {threshold:.2f}  (proba ≥ threshold => 1)")

    st.progress(min(max(proba, 0.0), 1.0))

  

    with st.expander("Ver linha enviada ao modelo"):
        st.dataframe(X_novo)

