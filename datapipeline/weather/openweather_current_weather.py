import os

from dotenv import load_dotenv

from Extract.weather.openweather_weather import fetch_current_weather
from Transform.weather.openweather_weather import weather_data_structure
from database.mongodb_functools import MongoDBManager
from database.postgresql_functools import PostgreSQLManager, Weather
from utils.json_functools import append_to_json
from utils.csv_functools import append_to_csv
from utils.openweather_functools import extract_lat_lon


if __name__ == '__main__':
    load_dotenv()
    dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    verbose = True

    api_key = os.getenv('OPEN_WEATHER_API_KEY')
    locations = os.getenv('LOCATIONS').split(',')
    country_code = os.getenv('COUNTRY_CODE')

    mongo_manager = MongoDBManager()
    postgre_manager = PostgreSQLManager()

    # Extract
    cities = mongo_manager.find_documents('city', {'country': country_code})
    latitudes, longitudes = extract_lat_lon(cities, country_code)
    weather = fetch_current_weather(latitudes, longitudes, api_key)

    for weather_dict in weather:
        city_id = postgre_manager.fetch_city_record_by_coord(
            weather_dict['coord']['lat'],
            weather_dict['coord']['lon']).id

        if verbose:
            append_to_json(weather_dict, os.path.join(dir_path, 'json', 'weatherInfo.json'))
        # Load
        mongo_manager.insert_document('weather', weather_dict)

        # Transform
        weather = weather_data_structure(weather_dict, city_id)
        if verbose:
            append_to_csv(weather, os.path.join(dir_path, 'csv', 'weatherInfo.csv'))
        # Load
        postgre_manager.add_record(Weather(**weather))
