from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import subprocess

# defining DAG
default_args = {
    'owner': 'chaima',
    'depends_on_past': False,
    'start_date': datetime(2026, 1, 16),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'smart_logitrack_dag',
    default_args=default_args,
    description='Pipeline for Smart LogiTrack: ETL to ML',
    schedule_interval='@daily',
    catchup=False
) as dag:

    #cleaning (silver)
    def run_cleaning():
        #running the script of cleaning
        subprocess.run(["python3", "/opt/airflow/scripts/clean_data.py"], check=True)

    #entrainement du model
    def run_training():
        # running the script of training
        subprocess.run(["python3", "/opt/airflow/scripts/train_model.py"], check=True)

    #define the tasks
    task_clean = PythonOperator(
        task_id='clean_and_save_silver',
        python_callable=run_cleaning
    )

    task_train = PythonOperator(
        task_id='train_and_save_model',
        python_callable=run_training
    )

    # order of execution
    task_clean >> task_train