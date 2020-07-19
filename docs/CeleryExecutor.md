### 1. Install Rabbitmq
```
apt-get update
apt-get upgrade
apt-get install erlang
apt-get install rabbitmq-server
systemctl enable rabbitmq-server
systemctl start rabbitmq-server
systemctl status rabbitmq-server
```

### 2. Setup user and console
```
sudo rabbitmqctl add_user rabbitmq rabbitmq
sudo rabbitmqctl set_user_tags rabbitmq administrator
sudo rabbitmqctl set_permissions -p / rabbitmq ".*" ".*" ".*"

sudo rabbitmq-plugins enable rabbitmq_management
sudo chown -R rabbitmq:rabbitmq /var/lib/rabbitmq/
```

### 3. Change in the airflow.cfg

```
executor = CeleryExecutor
broker_url = pyamqp://rabbitmq:rabbitmq@localhost/
result_backend = db+postgresql://$your_db_user:$your_db_password@$your_postgre#s_db_host:$postgres_port/$db_name
worker_log_server_port = 8793
```

### 4. Initialize the database and start airflow

```
airflow initdb
airflow scheduler
airflow webserver
airflow worker
airflow flower
```