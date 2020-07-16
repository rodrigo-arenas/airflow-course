# airflow-course
Repository for airflow course

### 1. Added airflow folder to pythonpath to use subfolders

```
export PYTHONPATH="${PYTHONPATH}:${AIRFLOW_HOME}"
```

### 2. Install packages
```
pip install "apache-airflow[celery, crypto, mysql, rabbitqm, redis, postgres]"
```

### 3. Initialize the db
```
airflow initdb
```
* Check new folder on the root user:
    ```
    cd airflow
    ```
### 4.Create dag and data_pipelines folder  
```
cd airflow
mkdir dags
mkdir data_pipelines
```
* optionally changed load_examples = False in airflow.cfg
##### WARNING: Only use if your db and dag folder is empty
    ```
    airflow resetdb
    ```
### 5. move files to dag and data_pipelines folder
```
cp dags/*.py /home/usr/airflow/dags
cp data_pipelines/*.py /home/$USER/airflow/data_pipelines
```

### 6. Start the scheduler and webserver
* User different terminals to run:
```
airflow scheduler
airflow webserver
```

### 7. Go to Airflow UI
http://0.0.0.0:8080/admin/


### 8. Run a test
```
airflow test twitter_dag fetching_tweets 2020-01-01
```