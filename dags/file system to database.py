from __future__ import annotations

import datetime
from airflow.models.dag import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.bash import BashOperator

meltano_extractor_root_path = '/home/jorge/Projects/Test/meltano-projects/extractor'
meltano_loader_root_path = '/home/jorge/Projects/Test/meltano-projects/loader'


default_args = {
    "owner": "jorge berti",
    "retries": 0    
}

with DAG(
    dag_id="file_system_to_database",
    dag_display_name = "Extraction data from file system to Postgres",
    catchup=False,
    default_args = default_args,
    dagrun_timeout=datetime.timedelta(minutes=60),
    tags=["el", "dev", "meltano"]
) as dag:    

    start = EmptyOperator(task_id="start")
    end = EmptyOperator(task_id="end")

    orders_details = BashOperator(
        task_id= "orders_details_to_database",
        bash_command=f" cd {meltano_loader_root_path} && meltano el tap-csv-orders_details target-postgres",        
    )

    employee_territories = BashOperator(
        task_id= "employee_territories_to_database",
        bash_command=f" cd {meltano_loader_root_path} && meltano el tap-csv-employee_territories target-postgres",        
    )

    categories = BashOperator(
        task_id= "categories_to_database",
        bash_command=f" cd {meltano_loader_root_path} && meltano el tap-csv-categories target-postgres",        
    )

    customers = BashOperator(
        task_id= "customers_to_database",
        bash_command=f" cd {meltano_loader_root_path} && meltano el tap-csv-customers target-postgres",        
    )

    employees = BashOperator(
        task_id= "employees_to_database",
        bash_command=f" cd {meltano_loader_root_path} && meltano el tap-csv-employees target-postgres",        
    )

    orders = BashOperator(
        task_id= "orders_to_database",
        bash_command=f" cd {meltano_loader_root_path} && meltano el tap-csv-orders target-postgres",        
    )

    products = BashOperator(
        task_id= "products_to_database",
        bash_command=f" cd {meltano_loader_root_path} && meltano el tap-csv-products target-postgres",        
    )

    region = BashOperator(
        task_id= "region_to_database",
        bash_command=f" cd {meltano_loader_root_path} && meltano el tap-csv-region target-postgres",        
    )

    shippers = BashOperator(
        task_id= "shippers_to_database",
        bash_command=f" cd {meltano_loader_root_path} && meltano el tap-csv-shippers target-postgres",        
    )

    suppliers = BashOperator(
        task_id= "suppliers_to_database",
        bash_command=f" cd {meltano_loader_root_path} && meltano el tap-csv-suppliers target-postgres",        
    )

    territories = BashOperator(
        task_id= "territories_to_database",
        bash_command=f" cd {meltano_loader_root_path} && meltano el tap-csv-territories target-postgres",        
    )

    us_states = BashOperator(
        task_id= "us_states_to_database",
        bash_command=f" cd {meltano_loader_root_path} && meltano el tap-csv-us_states target-postgres",        
    )

    start >> [categories,customers, employees, orders, products, region, shippers, suppliers, territories,
    us_states, employee_territories, orders_details] >> end