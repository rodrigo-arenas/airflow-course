from datetime import datetime, timedelta
from airflow import DAG
from airflow.hooks.postgres_hook import PostgresHook
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.python_operator import BranchPythonOperator
from airflow.operators.bash_operator import BashOperator

default_args = {
    'owner': 'airflow',
    'depend_on_past': False,
    'start_date': datetime(2020, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=1)
}


def get_activated_jobs():
    request = "SELECT * FROM dag"
    postgres_hook = PostgresHook(postgres_conn_id="psql_airflow_mdb",
                                 schema="airflow_mdb")  # This connection must be set from the Connection view in Airflow UI
    connection = postgres_hook.get_conn()  # Gets the connection from MySqlHook
    cursor = connection.cursor()  # Gets a cursor
    cursor.execute(request)  # Executes the request
    jobs = cursor.fetchall()  # Fetchs all the data from the executed request
    for job in jobs:  # Does a simple print of each source to show that the hook works well
        if not job[1]:
            return job[0]
        return None


def jobs_to_use(**kwargs):
    ti = kwargs['ti']
    job = ti.xcom_pull(task_ids='hook_task')
    print("job fetch from XCOM: {}".format(job))
    return job


def check_for_activated_job(**kwargs):
    ti = kwargs['ti']
    return ti.xcom_pull(task_ids='xcom_task').lower()


with DAG('branch_dag',
         default_args=default_args,
         schedule_interval='@once') as dag:
    start_task = DummyOperator(task_id='start_task')
    hook_task = PythonOperator(task_id='hook_task', python_callable=get_activated_jobs)
    xcom_task = PythonOperator(task_id='xcom_task', python_callable=jobs_to_use, provide_context=True)
    branch_task = BranchPythonOperator(task_id='branch_task', python_callable=check_for_activated_job,
                                       provide_context=True)
    subdag_dag = BashOperator(task_id='subdag_dag', bash_command='echo "subdag_dag is activated"')
    hello_world_dag = BashOperator(task_id='hello_world_dag', bash_command='echo "hello_world_dag is activated"')
    twitter_dag = BashOperator(task_id='twitter_dag', bash_command='echo "twitter_dag is activated"')
    simple_dag_backfill = BashOperator(task_id='simple_dag_backfill', bash_command='echo "simple_dag_backfill is activated"')

    start_task >> hook_task >> xcom_task >> branch_task
    branch_task >> subdag_dag
    branch_task >> hello_world_dag
    branch_task >> twitter_dag
    branch_task >> simple_dag_backfill
