### Common commands for airflow
+ list of commands
```
airflow -h
```

+ start web server and get access to UI
```
airflow webserver
```

+ start scheduler in the dags
```
airflow scheduler
```

+ start celery worker to run distributed airflow
```
airflow worker
```

+ get the list of dags 
```
airflow list_dags
```

+ get the task of a dag
```
airflow list_tasks "dag_name"
```

+ get tasks dependencies of task in a dag
```
airflow list_taks "dag_name" --tree
```