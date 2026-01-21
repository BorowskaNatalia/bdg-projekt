from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

DEFAULT_ARGS = {"owner": "airflow", "retries": 1, "retry_delay": timedelta(minutes=2)}

with DAG(
    dag_id="task1_sleep_simulation_to_postgres",
    description="Task 1: trigger simulation script and insert data into PostgreSQL",
    start_date=datetime(2025, 1, 1),
    schedule_interval="@hourly",  # albo "@daily"
    catchup=False,
    default_args=DEFAULT_ARGS,
) as dag:

    simulate = BashOperator(
        task_id="simulate_sleep_events",
        bash_command="python /opt/airflow/scripts/simulate_sleep_events.py",
    )

    insert_to_pg = BashOperator(
        task_id="insert_sleep_events_to_postgres",
        bash_command="python /opt/airflow/scripts/insert_sleep_events_to_postgres.py",
    )

    simulate >> insert_to_pg
