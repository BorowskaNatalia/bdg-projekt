import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

POSTGRES_USER = os.getenv("POSTGRES_USER", "bgd")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "bgd")
POSTGRES_DB = os.getenv("POSTGRES_DB", "bgd")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "bgd_postgres")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")

IN_CSV = os.getenv("SLEEP_EVENTS_CSV", "/opt/airflow/data/processed/sleep_events.csv")

def main():
    if not os.path.exists(IN_CSV):
        raise FileNotFoundError(f"Brak pliku events CSV: {IN_CSV}. Najpierw uruchom symulację.")

    df = pd.read_csv(IN_CSV)

    engine = create_engine(
        f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    )

    # append = “insert procesu do PostgreSQL”
    df.to_sql("sleep_events", engine, if_exists="append", index=False)
    print(f"OK: wrzucono {len(df)} rekordów do tabeli sleep_events")

if __name__ == "__main__":
    main()
