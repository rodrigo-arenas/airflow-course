# airflow-course
Repository for airflow course

### 1. Install packages
```
pip install "apache-airflow[celery, crypto, mysql, rabbitqm, redis]"
```

### 2. Initialize the db
```
airflow initdb
```
* Check new folder on the root user:
    ```
    cd airflow
    ```
### 3.Create dag folder  
```
cd airflow
mkdir dags
```
* optionally changed load_examples = False in airflow.cfg
##### WARNING: Only use if your db and dag folder is empty
    ```
    airflow resetdb
    ```
### 4. move files to dag folder
```
cp dags/*.py /home/usr/airflow/dags
```

### 5. Start the scheduler and webserver
* User different terminals to run:
```
airflow scheduler
airflow webserver
```

### G. Go to Airflow UI
http://0.0.0.0:8080/admin/
