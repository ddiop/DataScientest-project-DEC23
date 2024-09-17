# Ajouter le chemin du répertoire parent de Extract au chemin de recherche
import datetime

from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python import PythonOperator


from database.MongoClient import MongoDBConnection
from database import MongoClient

db = "airflow"
new_db = "france"
collection_countries = "countries"
from api import countries

def extract_countries():
    # Modify these parameters with your MongoDB connection details

    connection = MongoClient.MongoDBConnection()

    # Example data to insert

    countries_data = countries.get_api_data("https://api.thecompaniesapi.com/v1/locations/countries")
    print(countries_data)
    connection.insert_documents(db, collection_countries, countries_data[collection_countries])


def transform_countries():
    # Connexion à la base de données source
    print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
    source_client = MongoDBConnection()

    franc_info = source_client.get_documents_by_country(db, collection_countries, "France")

    # Connexion à la base de données cible
    target_client = MongoDBConnection()

    # Insertion des informations dans la nouvelle base de données
    target_client.insert_documents(new_db, "info_france", franc_info)
    print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')


with DAG(
        dag_id='extract_and_transform_dag',
        description='My DAG that\'s triggered every minute',
        tags=['poc', 'autralian_project'],
        schedule_interval='*/5 * * * *',
        default_args={
            'owner': 'airflow',
            'start_date': days_ago(0, minute=1),
        },
        catchup=False
) as open_weather_dag:
    extract_data_task = PythonOperator(
        task_id='extract_data_task',
        python_callable=extract_countries,
        retries=3,
        retry_delay=datetime.timedelta(seconds=30)


    )

    transform_data_task = PythonOperator(
        task_id='transform_data_task',
        python_callable=transform_countries,
        trigger_rule='all_success'
    )

    extract_data_task >> transform_data_task
