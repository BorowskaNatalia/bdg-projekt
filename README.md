# BGD Project - Task 0–1 (Airflow Orchestration)

This repo contains the initial setup for Project 2:
- Dockerized services (Airflow + PostgreSQL)
- Airflow DAG that runs a Python simulation and inserts generated data into PostgreSQL

## Services
- Airflow UI: http://localhost:8080 (login: airflow / airflow)
- BGD PostgreSQL: localhost:5432 (db: bgd, user: bgd)

## Dataset
We use the Kaggle Sleep Dataset (62 mammals). The dataset file should be available as:
- `data/raw/sleep.csv`

## Quick start
1) Start everything:
```bash
docker compose up -d
docker compose ps
```

Verify the dataset loader ran (auto container bgd_loader):

```bash

docker logs bgd_loader --tail 120
docker exec -it bgd_postgres psql -U bgd -d bgd -c "SELECT COUNT(*) FROM sleep_raw;"
```
Task 1 — Airflow DAG (simulation -> PostgreSQL)
What the DAG does
DAG: task1_sleep_simulation_to_postgres

simulate_sleep_events
Reads sleep_raw from PostgreSQL and generates a batch of events into:

/opt/airflow/data/processed/sleep_events.csv (mounted from ./data/processed/sleep_events.csv)

insert_sleep_events_to_postgres
Appends the generated events into PostgreSQL table:

sleep_events

Schedule
The DAG runs on an hourly schedule (configured in the DAG file).

Run the DAG
Open Airflow UI: http://localhost:8080

Find DAG: task1_sleep_simulation_to_postgres

Toggle ON and click Trigger DAG

Verify inserts
```bash
docker exec -it bgd_postgres psql -U bgd -d bgd -c "SELECT COUNT(*) FROM sleep_events;"
docker exec -it bgd_postgres psql -U bgd -d bgd -c "SELECT MAX(event_time_utc) FROM sleep_events;"
```
Project structure

.
├─ docker-compose.yml
├─ .env
├─ dags/
│  └─ sleep_simulation_to_postgres.py
├─ scripts/
│  ├─ load_sleep_to_postgres.py
│  ├─ simulate_sleep_events.py
│  └─ insert_sleep_events_to_postgres.py
├─ data/
│  ├─ raw/
│  │  └─ sleep.csv
│  └─ processed/
│     └─ sleep_events.csv
├─ logs/        # airflow logs
└─ plugins/     # airflow plugins

Notes
bgd_loader is a one-shot container that loads data/raw/sleep.csv into PostgreSQL as sleep_raw.

## Task 2.1 - MinIO (Bronze/Silver storage)
- MinIO Console: http://localhost:9001
- Bucket is created automatically by `minio-init` (bucket: bgd)

Run:
```bash
docker compose up -d minio minio-init
docker logs bgd_minio_init --tail 50
```