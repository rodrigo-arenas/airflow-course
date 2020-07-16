from airflow import DAG
from airflow.contrib.sensors.file_sensor import FileSensor
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
from data_pipelines import fetching_tweet

"""
On UI admin/connections/create must be a file conww shii, enection called fs_tweet
put on Extra: {"path: "/home/user/airflow/dags/data/"}
that is the location where data.csv will be searched

Run in terminal: airflow test twitter_dag waiting_for_tweets 2020-01-01
"""

default_args = {
    "start_date": datetime(2020, 7, 1),
    "owner": "airflow"
}

with DAG(dag_id="twitter_dag", schedule_interval="@daily", default_args=default_args) as dag:
    waiting_for_tweets = FileSensor(task_id="waiting_for_tweets",
                                    fs_conn_id="fs_tweet",
                                    filepath='data.csv',
                                    poke_interval=5)
    fetching_tweets = PythonOperator(task_id='fetching_tweets', python_callable=fetching_tweet.main)