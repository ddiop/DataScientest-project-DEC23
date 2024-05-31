import os

from database.mongodb_functools import MongoDBManager
from database.postgresql_functools import PostgreSQLManager, Weather
from utils.csv_functools import load_from_csv
from utils.json_functools import load_from_json


def load_weather():
    mongo_manager = MongoDBManager()
    [mongo_manager.insert_document('Weather', weather)
     for weather in load_from_json(os.path.join('json', 'WeatherInfo.json'))]

    postgre_manager = PostgreSQLManager()
    [postgre_manager.add_record(Weather(**weather))
     for weather in load_from_csv(os.path.join('csv', 'WeatherInfo.csv'))]
