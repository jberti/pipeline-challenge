from __future__ import annotations

import datetime

import pendulum

from airflow.models.dag import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.bash import BashOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
import subprocess
from airflow.operators.python import PythonOperator
from pathlib import Path

meltano_extractor_root_path = '/home/jorge/Projects/Test/meltano-projects/extractor'
meltano_loader_root_path = '/home/jorge/Projects/Test/meltano-projects/loader'

default_meltano_root_path = Path(__file__).parent / "meltano-projects" / "extractor"


default_args = {
    "owner": "jorge berti",
    "retries": 0    
}

def meltano_calls(dag):
    list = {
        'tap-csv': 'target-csv-from-csv',
        'tap-postgres-customers' : 'target-csv-customers',
        'tap-postgres-employees' : 'target-csv-employees',
        'tap-postgres-orders' : 'target-csv-orders',
        'tap-postgres-products' : 'target-csv-products',
        'tap-postgres-region' : 'target-csv-region',
        'tap-postgres-shippers' : 'target-csv-shippers',
        'tap-postgres-suppliers' : 'target-csv-suppliers',
        'tap-postgres-territories' : 'target-csv-territories',
        'tap-postgres-us_states' : 'target-csv-us_states',
        'tap-postgres-categories' : 'target-csv-categories',
        'tap-postgres-customer_customer_demo' : 'target-csv-customer_customer_demo',
        'tap-postgres-employee_territories' : 'target-csv-employee_territories'
    }

    for key, value in list.items():
        task = PythonOperator( 
                task_id=f'process_{key}',
                python_callable=bash_call(f" cd {default_meltano_root_path} && meltano el {key} {value}"),
                op_args=[key, value],
                dag=dag
            )

def bash_call(command):
    """Runs a bash command and returns the result."""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
        return result.stdout.strip()  # Return stdout, removing leading/trailing whitespace
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        print(f"Stderr: {e.stderr}")  # Print stderr for debugging
        return None  # Or raise the exception if you want to halt execution

with DAG(
    dag_id="data_to_file_system",
    dag_display_name = "Extraction data to file system",    
    start_date=pendulum.datetime(2024, 10, 22),
    schedule_interval='@daily',
    catchup=False,
    default_args = default_args,
    dagrun_timeout=datetime.timedelta(minutes=60),
    tags=["el", "dev", "meltano"],
    params={"Start date": "date"}
) as dag:

    start = EmptyOperator(task_id="start")
    end = EmptyOperator(task_id="end")

    meltano_calls(dag)

    trigger = TriggerDagRunOperator(

        task_id="trigger-to-database",

        trigger_dag_id="file_system_to_database",  # Ensure this equals the dag_id of the DAG to trigger

        conf={"message": "Done first part"},

    )

    start >> meltano_calls(dag) >> trigger >> end