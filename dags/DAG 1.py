from __future__ import annotations

import datetime

import pendulum

from airflow.models.dag import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.bash import BashOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator

meltano_extractor_root_path = '/home/jorge/Projects/Test/meltano-projects/extractor'
meltano_loader_root_path = '/home/jorge/Projects/Test/meltano-projects/loader'


default_args = {
    "owner": "jorge berti",
    "retries": 0    
}

with DAG(
    dag_id="data_to_file_system",
    dag_display_name = "Extraction data to file system",    
    start_date=pendulum.datetime(2024, 10, 22),
    schedule_interval='@daily'
    catchup=False,
    default_args = default_args,
    dagrun_timeout=datetime.timedelta(minutes=60),
    tags=["el", "dev", "meltano"],
    params={"Start date": "date"},
) as dag:

    start = EmptyOperator(task_id="start")
    end = EmptyOperator(task_id="end")

    csv_file_to_csv = BashOperator(
        task_id="csv_file_to_csv",            
        bash_command=f" cd {meltano_extractor_root_path} && meltano el tap-csv target-csv-from-csv",        
    ) 

    customers_to_csv = BashOperator(
        task_id="customers_to_csv",            
        bash_command=f" cd {meltano_extractor_root_path} && meltano el tap-postgres-customers target-csv-customers",        
    ) 

    employees_to_csv = BashOperator(
        task_id="employees_to_csv",            
        bash_command=f" cd {meltano_extractor_root_path} && meltano el tap-postgres-employees target-csv-employees",        
    )

    orders_to_csv = BashOperator(
        task_id="orders_to_csv",            
        bash_command=f" cd {meltano_extractor_root_path} && meltano el tap-postgres-orders target-csv-orders",        
    )

    products_to_csv = BashOperator(
        task_id="products_to_csv",            
        bash_command=f" cd {meltano_extractor_root_path} && meltano el tap-postgres-products target-csv-products",        
    )

    region_to_csv = BashOperator(
        task_id="region_to_csv",            
        bash_command=f" cd {meltano_extractor_root_path} && meltano el tap-postgres-region target-csv-region",        
    )

    shippers_to_csv = BashOperator(
        task_id="shippers_to_csv",            
        bash_command=f" cd {meltano_extractor_root_path} && meltano el tap-postgres-shippers target-csv-shippers",        
    )

    suppliers_to_csv = BashOperator(
        task_id="suppliers_to_csv",            
        bash_command=f" cd {meltano_extractor_root_path} && meltano el tap-postgres-suppliers target-csv-suppliers",        
    )

    territories_to_csv = BashOperator(
        task_id="territories_to_csv",            
        bash_command=f" cd {meltano_extractor_root_path} && meltano el tap-postgres-territories target-csv-territories",        
    )

    us_states_to_csv = BashOperator(
        task_id="us_states_to_csv",            
        bash_command=f" cd {meltano_extractor_root_path} && meltano el tap-postgres-us_states target-csv-us_states",        
    )

    categories_to_csv = BashOperator(
        task_id="categories_to_csv",            
        bash_command=f" cd {meltano_extractor_root_path} && meltano el tap-postgres-categories target-csv-categories",        
    )

    customer_customer_demo_to_csv = BashOperator(
        task_id="customer_customer_demo_to_csv",            
        bash_command=f" cd {meltano_extractor_root_path} && meltano el tap-postgres-customer_customer_demo target-csv-customer_customer_demo",        
    )

    employee_territories_to_csv = BashOperator(
        task_id="employee_territories_to_csv",            
        bash_command=f" cd {meltano_extractor_root_path} && meltano el tap-postgres-employee_territories target-csv-employee_territories",        
    )

    trigger = TriggerDagRunOperator(

        task_id="trigger-to-database",

        trigger_dag_id="file_system_to_database",  # Ensure this equals the dag_id of the DAG to trigger

        conf={"message": "Done first part"},

    )

    start >> [csv_file_to_csv,categories_to_csv, customers_to_csv, employees_to_csv,orders_to_csv,products_to_csv,
    region_to_csv,shippers_to_csv,suppliers_to_csv,territories_to_csv,us_states_to_csv,customer_customer_demo_to_csv,employee_territories_to_csv] >> trigger >> end

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