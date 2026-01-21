import os
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

POSTGRES_USER = os.getenv("POSTGRES_USER", "bgd")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "bgd")
POSTGRES_DB = os.getenv("POSTGRES_DB", "bgd")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")

CSV_PATH = os.getenv("SLEEP_CSV_PATH", "data/raw/sleep.csv")

def main():
    if not os.path.exists(CSV_PATH):
        raise FileNotFoundError(
            f"Brak pliku: {CSV_PATH}\n"
            f"Wrzuć CSV do data/raw/ jako sleep.csv (albo ustaw SLEEP_CSV_PATH)."
        )

    df = pd.read_csv(CSV_PATH)
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

    engine = create_engine(
        f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    )

    df.to_sql("sleep_raw", engine, if_exists="replace", index=False)

    with engine.connect() as conn:
        count = conn.execute(text("SELECT COUNT(*) FROM sleep_raw")).scalar_one()

    print(f"OK: zapisano {count} rekordów do tabeli sleep_raw")

if __name__ == "__main__":
    main()
