# src/export_processed.py

import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

def export_processed():
    # Dados do banco (vem do .env)
    host = os.getenv("DB_HOST", "localhost")
    port = os.getenv("DB_PORT", "5432")
    dbname = os.getenv("DB_NAME", "tech_challenge_fase4")
    user = os.getenv("DB_USER")
    pwd = os.getenv("DB_PASS")
    schema = os.getenv("DB_SCHEMA", "public")
    table = os.getenv("DB_TABLE", "obesidade")

    if not user or not pwd:
        raise ValueError("DB_USER e/ou DB_PASS não definidos no .env")

    url = f"postgresql+psycopg2://{user}:{pwd}@{host}:{port}/{dbname}"
    engine = create_engine(url)

    query = f'SELECT * FROM "{schema}"."{table}"'
    df = pd.read_sql(query, con=engine)

    os.makedirs("data/processed", exist_ok=True)
    out_path = "data/processed/obesity_processed_postgres.csv"
    df.to_csv(out_path, index=False, encoding="utf-8")

    print(f"Arquivo gerado: {out_path}")
    print(f"Linhas: {len(df)} | Colunas: {len(df.columns)}")

if __name__ == "__main__":
    export_processed()
