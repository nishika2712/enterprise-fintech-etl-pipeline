from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

# Default arguments for the Airflow DAG
default_args = {
    'owner': 'nishika-jain',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'fintech_etl_pipeline_dag',
    default_args=default_args,
    description='Orchestrates the PySpark Fintech ETL and Data Quality validation pipeline',
    schedule_interval='@daily',
    start_date=datetime(2026, 1, 1),
    catchup=False,
) as dag:

    # Task 1: Run automated data quality unit tests via Pytest
    run_pytest = BashOperator(
        task_id='run_unit_tests',
        bash_command='pytest tests/',
    )

    # Task 2: Run the PySpark ETL transformation pipeline
    run_spark_etl = BashOperator(
        task_id='run_pyspark_transformation',
        bash_command='python etl/transform_spark.py',
    )

    # Define task dependencies (Task 1 must succeed before Task 2 runs)
    run_pytest >> run_spark_etl