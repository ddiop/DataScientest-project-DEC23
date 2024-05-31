import os

from database.postgresql_functools import PostgreSQLManager, AustralianMeteorologyWeather
from utils.csv_functools import load_from_csv


def load_australian_meteorology_weather():
    postgre_manager = PostgreSQLManager()
    [postgre_manager.add_record(AustralianMeteorologyWeather(**weather))
     for weather in load_from_csv(os.path.join('csv', 'AustralianMeteorologyWeatherInfo.csv'))]
