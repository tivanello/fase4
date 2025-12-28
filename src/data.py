import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

def load_from_postgres() -> pd.DataFrame:
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    name = os.getenv("DB_NAME")
    user = os.getenv("DB_USER")
    pwd  = os.getenv("DB_PASS")
    schema = os.getenv("DB_SCHEMA", "public")
    table  = os.getenv("DB_TABLE")

    if not table:
        raise ValueError("DB_TABLE não definido no .env")

    url = f"postgresql+psycopg2://{user}:{pwd}@{host}:{port}/{name}"
    engine = create_engine(url)

    query = f'SELECT * FROM "{schema}"."{table}"'
    return pd.read_sql(query, con=engine)

def load_data() -> pd.DataFrame:
    """
    DATA_SOURCE:
      - postgres        -> lê do PostgreSQL
      - processed_csv   -> lê do CSV tratado em data/processed/
      - csv (ou outro)  -> fallback para o raw do enunciado
    """
    source = os.getenv("DATA_SOURCE", "postgres").lower()

    if source == "postgres":
        return load_from_postgres()

    if source == "processed_csv":
        return pd.read_csv("data/processed/obesity_processed_postgres.csv")

    # fallback (raw)
    return pd.read_csv("data/raw/obesity.csv")
