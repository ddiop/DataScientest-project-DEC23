import json
import os
from pathlib import Path

from dotenv import load_dotenv

from Transform.weather.openweather_weather import previous_timestamp_weather_data_structure
from database.mongodb_functools import MongoDBManager
from database.postgresql_functools import PostgreSQLManager, Weather
from utils.csv_functools import load_from_csv, append_to_csv
from utils.json_functools import append_to_json, load_from_json


def load_weather():
    mongo_manager = MongoDBManager()
    [mongo_manager.insert_document('weather', weather)
     for weather in load_from_json(os.path.join('dataJson', 'WeatherInfo.json'))]

    postgre_manager = PostgreSQLManager()
    [postgre_manager.add_record(Weather(**weather))
     for weather in load_from_csv(os.path.join('dataCsv', 'WeatherInfo.csv'))]


def load_weather_to_datalake():
    """
    Only for Laurent's data
    """
    dir_path = Path(__file__).parents[1]
    verbose = True
    load_dotenv()
    mongo_manager = MongoDBManager()
    with open(os.path.join(dir_path, 'dataJson', 'dataWeatherTimeStamp.json'), 'r') as f:
        for line in f:
            weather_dict = json.loads(line)
            if verbose:
                append_to_json(weather_dict, os.path.join(dir_path, 'dataJson', 'weatherInfo.json'))
            mongo_manager.insert_document('weather', weather_dict)


def load_weather_to_datawarehouse():
    """
    Only for Laurent's data
    """
    dir_path = Path(__file__).parents[1]
    verbose = True
    load_dotenv()
    postgre_manager = PostgreSQLManager()

    with open(os.path.join(dir_path, 'dataJson', 'dataWeatherTimeStamp.json'), 'r') as f:
        for line in f:
            weather_dict = json.loads(line)
            city_id = postgre_manager.fetch_city_record_by_coord(
                weather_dict['lat'],
                weather_dict['lon']).id

            weather = previous_timestamp_weather_data_structure(weather_dict, city_id)
            if verbose:
                append_to_csv(weather, os.path.join(dir_path, 'dataCsv', 'weatherInfo.csv'))
            postgre_manager.add_record(Weather(**weather))


load_weather_to_datalake()
load_weather_to_datawarehouse()
