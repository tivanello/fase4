# app_obesidade.py
import streamlit as st
import pandas as pd
import numpy as np
import joblib

# =======================
# CONFIG
# =======================
st.set_page_config(page_title="App Obesidade", page_icon="🍽️", layout="centered")

MODEL_PATH = r"C:\projetos\fase4\models\modelo_rf.joblib"
FEATURES_CSV = r"C:\projetos\fase4\data\features\obesidade_features.csv"

st.markdown(
    "<style>div[role='listbox'] ul{background-color: #6e42ad};</style>",
    unsafe_allow_html=True
)

st.markdown(
    "<h1 style='text-align: center;'>Questionário de Tendência à Obesidade 🍽️</h1>",
    unsafe_allow_html=True
)

st.info("Preencha e clique em **Avaliar**. O modelo retorna tendência (0/1) e probabilidade de obesidade.")

# =======================
# LOAD MODEL (artefato)
# =======================
@st.cache_resource
@st.cache_resource
def carregar_artefato(caminho: str):
    artefato = joblib.load(caminho)
    model = artefato.get("model", artefato)
    feature_columns = artefato.get("feature_columns")
    threshold = float(artefato.get("threshold", 0.5))
    return model, feature_columns, threshold

model, feature_columns, threshold = carregar_artefato(MODEL_PATH)

# ======== MAPAS PARA UI AMIGÁVEL (AJUSTE SE SEUS CÓDIGOS FOREM DIFERENTES) ========
MAPA_SEXO_UI = {"Feminino": 0, "Masculino": 1}
MAPA_SIM_NAO_UI = {"Não": 0, "Sim": 1}
MAPA_FREQUENCIA_0_3_UI = {"Nunca": 0, "Às vezes": 1, "Frequentemente": 2, "Sempre": 3}
MAPA_TEMPO_TELA_0_2_UI = {"Menos de 1 hora por dia": 0, "de 1 a 3 horas por dia": 1, "mais de 3 horas por dia": 2}
MAPA_TRANSPORTE_0_4_UI = {"Caminhando": 0, "Bicicleta": 1, "Transporte público": 2, "Automóvel": 3, "Moto": 4}
MAPA_NIVEL_1_3_UI = {"Baixo (1)": 1, "Médio (2)": 2, "Alto (3)": 3}
MAPA_REFEICOES_UI = {"1": 1, "2": 2, "3": 3, "4": 4, "5": 5}
MAPA_ATIVIDADE_0_3_UI = {"Nenhuma": 0, "Uma Vez por semana": 1, "duas a três vezes por semana": 2, "Mais de três vezes por semana": 3}
MAPA_ALCOOL_0_3_UI = {"Não bebo": 0, "Às vezes (1)": 1, "Frequentemente (2)": 2, "Sempre (3)": 3}


# =======================
# LOAD FEATURES CSV (opcional)
# =======================
@st.cache_data
def carregar_base_features(caminho_csv: str):
    try:
        df = pd.read_csv(caminho_csv)
        return df
    except Exception:
        return None

try:
    model, feature_columns, threshold = carregar_artefato(MODEL_PATH)
except Exception as e:
    st.error(f"Erro ao carregar o modelo em: {MODEL_PATH}\n\n{e}")
    st.stop()

df_ref = carregar_base_features(FEATURES_CSV)

# Colunas esperadas (as suas)
COLS = [
    "sexo", "idade", "historico_familiar", "ingere_alim_calorico",
    "ingere_vegetais", "qtd_refeicao_principal", "come_entre_refeicao",
    "fumante", "consumo_agua_litro", "monitora_calorias",
    "freq_atividade_fisica", "tempo_uso_eletronico",
    "frequencia_consumo_alcool", "meio_de_transporte"
]

# Se o artefato trouxe feature_columns, usa como fonte de verdade
if feature_columns is not None:
    COLS = list(feature_columns)

def _uniques(col, fallback):
    if df_ref is None or col not in df_ref.columns:
        return fallback
    vals = sorted(pd.Series(df_ref[col].dropna().unique()).tolist())
    return vals if len(vals) > 0 else fallback

def _minmax(col, fallback_min, fallback_max):
    if df_ref is None or col not in df_ref.columns:
        return fallback_min, fallback_max
    s = pd.to_numeric(df_ref[col], errors="coerce").dropna()
    if s.empty:
        return fallback_min, fallback_max
    return float(s.min()), float(s.max())

# =======================
# FORM
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
        ingere_vegetais_txt = st.selectbox("Ingestão de vegetais", list(MAPA_NIVEL_1_3_UI.keys()), index=1)
        qtd_refeicao_principal_txt = st.selectbox("Refeições principais por dia", list(MAPA_REFEICOES_UI.keys()), index=2)
        consumo_agua_litro_txt = st.selectbox("Consumo de água", list(MAPA_NIVEL_1_3_UI.keys()), index=1)

    with col6:
        freq_atividade_fisica_txt = st.selectbox("Atividade física", list(MAPA_ATIVIDADE_0_3_UI.keys()), index=1)
        tempo_uso_eletronico_txt = st.selectbox("Tempo diário de telas", list(MAPA_TEMPO_TELA_0_2_UI.keys()), index=1)

    submit = st.form_submit_button("Avaliar")
# =======================
# PREDICT
# =======================
if submit:
    linha = {
        "sexo": MAPA_SEXO_UI[sexo_txt],
        "idade": float(idade),
        "historico_familiar": MAPA_SIM_NAO_UI[historico_familiar_txt],
        "ingere_alim_calorico": MAPA_SIM_NAO_UI[ingere_alim_calorico_txt],
        "ingere_vegetais": MAPA_NIVEL_1_3_UI[ingere_vegetais_txt],
        "qtd_refeicao_principal": MAPA_REFEICOES_UI[qtd_refeicao_principal_txt],
        "come_entre_refeicao": MAPA_FREQUENCIA_0_3_UI[come_entre_refeicao_txt],
        "fumante": MAPA_SIM_NAO_UI[fumante_txt],
        "consumo_agua_litro": MAPA_NIVEL_1_3_UI[consumo_agua_litro_txt],
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

    st.write("---")
    st.write("## Resultado")

    st.metric("Probabilidade estimada de obesidade", f"{int(round(proba*100))}%")
    st.caption(f"Threshold usado: {threshold:.2f}  (proba ≥ threshold => 1)")

    st.progress(min(max(proba, 0.0), 1.0))

    if pred == 1:
        st.error("### Tendência: **Obeso (1)**")
    else:
        st.success("### Tendência: **Não obeso (0)**")

    with st.expander("Ver linha enviada ao modelo"):
        st.dataframe(X_novo)
