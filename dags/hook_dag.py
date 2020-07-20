from datetime import datetime, timedelta
from airflow import DAG
from airflow.hooks.postgres_hook import PostgresHook
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator

default_args = {
    'owner': 'airflow',
    'depend_on_past': False,
    'start_date': datetime(2020, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=1)
}


def get_activated_jobs():
    request = "SELECT * FROM job"
    postgres_hook = PostgresHook(postgres_conn_id="psql_airflow_mdb",
                                 schema="airflow_mdb")  # This connection must be set from the Connection view in Airflow UI
    connection = postgres_hook.get_conn()  # Gets the connection from MySqlHook
    cursor = connection.cursor()  # Gets a cursor
    cursor.execute(request)  # Executes the request
    jobs = cursor.fetchall()  # Fetchs all the data from the executed request
    for job in jobs:  # Does a simple print of each source to show that the hook works well
        print("jobs: {0} - activated: {1}".format(job[0], job[1]))
    return jobs


with DAG('hook_dag',
         default_args=default_args,
         schedule_interval='@once',
         catchup=False) as dag:
    start_task = DummyOperator(task_id='start_task')
    hook_task = PythonOperator(task_id='hook_task', python_callable=get_activated_jobs)
    start_task >> hook_task
