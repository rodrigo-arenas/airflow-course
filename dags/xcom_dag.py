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


# Read the table jobs to fetch the data and return the name of first source having its column "activated" sets to true
# No need to call xcom_push here since we use the keyword "return" which has the same effect.
def get_activated_jobs():
    request = "SELECT * FROM dag"
    postgres_hook = PostgresHook(postgres_conn_id="psql_airflow_mdb",
                                 schema="airflow_mdb")  # This connection must be set from the Connection view in Airflow UI
    connection = postgres_hook.get_conn()  # Gets the connection from MySqlHook
    cursor = connection.cursor()  # Gets a cursor
    cursor.execute(request)  # Executes the request
    jobs = cursor.fetchall()  # Fetchs all the data from the executed request
    for job in jobs:  # Does a simple print of each source to show that the hook works well
        return job[0]


def jobs_to_use(**kwargs):
    ti = kwargs['ti']
    job = ti.xcom_pull(task_ids='hook_task')
    print("job fetch from XCOM: {}".format(job))


with DAG('xcom_dag',
         default_args=default_args,
         schedule_interval='@once',
         catchup=False) as dag:
    start_task = DummyOperator(task_id='start_task')
    hook_task = PythonOperator(task_id='hook_task', python_callable=get_activated_jobs)
    xcom_task = PythonOperator(task_id='xcom_task', python_callable=jobs_to_use, provide_context=True)
    start_task >> hook_task >> xcom_task
