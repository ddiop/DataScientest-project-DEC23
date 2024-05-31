import os

from dotenv import load_dotenv

from Extract.city.openweather_city import build_city_url
from Transform.city.openweather_city import city_data_structure
from database.mongodb_functools import MongoDBManager
from database.postgresql_functools import PostgreSQLManager, City
from utils.json_functools import append_to_json
from utils.csv_functools import append_to_csv
from utils.openweather_functools import fetch_api_data


if __name__ == '__main__':
    load_dotenv()
    dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    verbose = True

    api_key = os.getenv('OPEN_WEATHER_API_KEY')
    locations = os.getenv('LOCATIONS').split(',')
    country_code = os.getenv('COUNTRY_CODE')

    mongo_manager = MongoDBManager()
    postgre_manager = PostgreSQLManager()

    for city_name in locations:
        city_json = fetch_api_data(build_city_url(city_name, api_key))[0]
        if verbose:
            append_to_json(city_json, os.path.join(dir_path, 'json', 'CityInfo.json'))
        mongo_manager.insert_document('City', city_json)

        city = city_data_structure(city_json)
        if verbose:
            append_to_csv(city, os.path.join(dir_path, 'csv', 'CityInfo.csv'))
        postgre_manager.add_record(City(**city))
