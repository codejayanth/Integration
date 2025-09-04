from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
import requests

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 9, 4),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
dag = DAG(
    'fetch_and_store_energinet_data',
    default_args=default_args,
    description='A DAG to fetch Energinet data and store it in Postgres',
    schedule=timedelta(days=1),
)

# Function to fetch data from the Energinet API
def fetch_energinet_data(ti):
    # Fetch data from the Energinet API
    response = requests.get(
        url='https://api.energidataservice.dk/dataset/CO2Emis?limit=5'
    )

    # Check if the request was successful
    if response.status_code != 200:
        raise ValueError(f"Failed to fetch data from API. Status code: {response.status_code}")

    # Parse the JSON response
    result = response.json()

    # Extract the 'records' field
    records = result.get('records', [])

    # Log the records for debugging
    print('Fetched records:')
    for record in records:
        print(' ', record)

    # Push the records to XCom for downstream tasks
    ti.xcom_push(key='energinet_data', value=records)

# Function to insert data into the Postgres table
def insert_energinet_data_into_postgres(ti):
    # Pull data from XCom
    energinet_data = ti.xcom_pull(key='energinet_data', task_ids='fetch_energinet_data')
    if not energinet_data:
        raise ValueError("No data found in XCom for task 'fetch_energinet_data'")

    # Initialize PostgresHook
    postgres_hook = PostgresHook(postgres_conn_id='books_connection')

    # SQL query for inserting data
    insert_query = """
    INSERT INTO energinet_data (Minutes5UTC, Minutes5DK, PriceArea, CO2Emission)
    VALUES (%s, %s, %s, %s)
    """

    # Insert each record into the table
    for record in energinet_data:
        postgres_hook.run(insert_query, parameters=(
            record['Minutes5UTC'],
            record['Minutes5DK'],
            record['PriceArea'],
            record['CO2Emission']
        ))

# Task to create the table if it doesn't exist
create_table_task = SQLExecuteQueryOperator(
    task_id='create_table',
    conn_id='books_connection',  # Updated to use conn_id
    sql="sql/energinet_schema.sql",  # Reference the external SQL file
    dag=dag,
)

# Task to fetch data from the API
fetch_energinet_data_task = PythonOperator(
    task_id='fetch_energinet_data',
    python_callable=fetch_energinet_data,
    dag=dag,
)

# Task to insert data into the Postgres table
insert_energinet_data_task = PythonOperator(
    task_id='insert_energinet_data',
    python_callable=insert_energinet_data_into_postgres,
    dag=dag,
)

# Define task dependencies
create_table_task >> fetch_energinet_data_task >> insert_energinet_data_task