from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.sensors.filesystem import FileSensor
from airflow.operators.docker_operator import DockerOperator
from docker.types import Mount
from airflow.operators.postgres_operator import PostgresOperator
from datetime import datetime, date

ENVIRONMENT = {
    'MONGO_INITDB_ROOT_USERNAME': 'admin',
    'MONGO_INITDB_ROOT_PASSWORD': 'adminpassword',

    'MONGO_INITDB_DATABASE': 'opendb',
    'MONGO_HOST': 'mongo',
    'MONGO_PORT': '27017',
    'POSTGRES_DB': 'lol',
    'POSTGRES_USER ': 'airflow',
    'POSTGRES_PASSWORD': 'airflow',
    'PG_HOST': 'postgres',


}

with DAG(
        dag_id='load_data',
        tags=['extract', 'load', 'DataScientest-project-DEC23'],
        default_args={
            'owner': 'airflow',
            'start_date': days_ago(0, minute=1),
        },

        catchup=False
) as dag:
    extract_city = DockerOperator(
        task_id='extract_city_data',
        image='datascientest_project_dec23:latest',
        auto_remove=True,
        command='python3 /app/preparation/city_from_openweather.py',
        network_mode='backend',
        environment=ENVIRONMENT
    )

    extract_air_pollution = DockerOperator(
        task_id='extract_air_pollution_data',
        image='datascientest_project_dec23:latest',
        auto_remove=True,
        command='python3 /app/preparation/air_pollution_from_openweather.py',
        network_mode='backend',
        environment=ENVIRONMENT
    )

    extract_weather_from_openweather = DockerOperator(
        task_id='extract_weather_from_openweather_data',
        image='datascientest_project_dec23:latest',
        auto_remove=True,
        command='python3 /app/preparation/weather_from_openweather.py',
        network_mode='backend',
        environment=ENVIRONMENT
    )
[extract_city, extract_air_pollution] >> extract_weather_from_openweather
