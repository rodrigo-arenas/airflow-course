from airflow import DAG
from airflow.contrib.sensors.file_sensor import FileSensor
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
from airflow.operators.postgres_operator import PostgresOperator
from datetime import datetime
from data_pipelines import fetching_tweet, cleaning_tweet

"""
On UI admin/connections/create must be a file conww shii, enection called fs_tweet
put on Extra: {"path: "/home/user/airflow/dags/data/"}
that is the location where data.csv will be searched

Run in terminal: airflow test twitter_dag waiting_for_tweets 2020-01-01

psql_airflow is an airflow connection to a postgresql database with a airflow_demo db and table "tweets"
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

    cleaning_tweets = PythonOperator(task_id='cleaning_tweets', python_callable=cleaning_tweet.main)

    storing_tweets = BashOperator(task_id='storing_tweets',
                                  bash_command="cp /tmp/data_cleaned.csv /home/$USER/airflow/dags/data")

    loading_tweets = PostgresOperator(task_id='loading_tweets',
                                      postgres_conn_id='psql_airflow',
                                      database='airflow_demo',
                                      sql="COPY tweets FROM '/tmp/data_cleaned.csv' WITH ("
                                          "FORMAT csv, HEADER TRUE, DELIMITER ',', ENCODING 'LATIN1');")
