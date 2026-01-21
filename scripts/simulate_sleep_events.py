import os
import uuid
from datetime import datetime, timezone

import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

POSTGRES_USER = os.getenv("POSTGRES_USER", "bgd")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "bgd")
POSTGRES_DB = os.getenv("POSTGRES_DB", "bgd")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "bgd_postgres")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")

OUT_CSV = os.getenv("SLEEP_EVENTS_CSV", "/opt/airflow/data/processed/sleep_events.csv")
N_SAMPLES = int(os.getenv("SLEEP_EVENT_SAMPLES", "200"))

def main():
    os.makedirs(os.path.dirname(OUT_CSV), exist_ok=True)

    engine = create_engine(
        f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    )

    df = pd.read_sql("SELECT * FROM sleep_raw", engine)
    if df.empty:
        raise RuntimeError("Tabela sleep_raw jest pusta. Najpierw wykonaj Task 0 loader (sleep_raw).")

    # symulacja = bierzemy losowe zwierzęta i robimy "event" z timestampem
    sample = df.sample(n=min(N_SAMPLES, len(df)), replace=(len(df) < N_SAMPLES), random_state=None).copy()

    now_utc = datetime.now(timezone.utc)
    batch_id = str(uuid.uuid4())

    sample["event_id"] = [str(uuid.uuid4()) for _ in range(len(sample))]
    sample["event_time_utc"] = now_utc.isoformat()
    sample["batch_id"] = batch_id

    # mały porządek nazw (czasem Kaggle ma spacje)
    sample.columns = [c.strip().lower().replace(" ", "_") for c in sample.columns]

    sample.to_csv(OUT_CSV, index=False)
    print(f"OK: wygenerowano {len(sample)} eventów -> {OUT_CSV} (batch_id={batch_id})")

if __name__ == "__main__":
    main()
