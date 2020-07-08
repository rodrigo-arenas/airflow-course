from airflow import DAG


with DAG(dag_id="twitter_dag", schedule_interval="@daily") as dag:
    None
