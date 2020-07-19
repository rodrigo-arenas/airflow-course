### 1. Change in the airflow.cfg

```
executor = LocalExecutor
sql_alchemy_conn = postgresql+psycopg2://$your_db_user:$your_db_password@$your_postgre#s_db_host:$postgres_port/$db_name
```

### 2. Create database and assign permissions to airflow user

```
CREATE DATABASE airflow OWNER airflow;
```

### 3. Initialize the database

```
airflow initdb
```
