import os

from database.mongodb_functools import MongoDBManager
from database.postgresql_functools import PostgreSQLManager, DailyWeather
from utils.csv_functools import load_from_csv
from utils.json_functools import load_from_json


def load_daily_weather():
    mongo_manager = MongoDBManager()
    [mongo_manager.insert_document('DailyWeather', weather)
     for weather in load_from_json(os.path.join('json', 'DailyWeatherInfo.json'))]

    postgre_manager = PostgreSQLManager()
    [postgre_manager.add_record(DailyWeather(**weather))
     for weather in load_from_csv(os.path.join('csv', 'DailyWeatherInfo.csv'))]
