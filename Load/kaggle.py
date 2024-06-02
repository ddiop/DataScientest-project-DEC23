import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv

from database.postgresql_functools import PostgreSQLManager, AustralianMeteorologyWeather


def load_kaggle_to_datawarehouse():
    dir_path = Path(__file__).parents[1]
    load_dotenv()
    postgre_manager = PostgreSQLManager()
    df = (pd.read_csv(os.path.join(dir_path, 'dataCsv', 'weatherAUS.csv'))
          .drop(columns=['RainToday', 'RainTomorrow']))
    df = df.rename(columns={'Date': 'date', 'Location': 'location', 'MinTemp': 'min_temp',
                            'MaxTemp': 'max_temp', 'Rainfall': 'rainfall',
                            'Evaporation': 'evaporation', 'Sunshine': 'sunshine',
                            'WindGustDir': 'wind_gust_dir', 'WindGustSpeed': 'wind_gust_speed',
                            'WindDir9am': 'wind_dir_9am', 'WindDir3pm': 'wind_dir_3pm',
                            'WindSpeed9am': 'wind_speed_9am', 'WindSpeed3pm': 'wind_speed_3pm',
                            'Humidity9am': 'humidity_9am', 'Humidity3pm': 'humidity_3pm',
                            'Pressure9am': 'pressure_9am', 'Pressure3pm': 'pressure_3pm',
                            'Cloud9am': 'cloud_9am', 'Cloud3pm': 'cloud_3pm', 'Temp9am': 'temp_9am',
                            'Temp3pm': 'temp_3pm'})
    [postgre_manager.add_record(AustralianMeteorologyWeather(**weather))
     for weather in df.to_dict(orient='records')]
    df.to_csv(os.path.join(dir_path, 'dataCsv', 'australianMeteorologyWeatherInfo.csv'),
              index=False)


load_kaggle_to_datawarehouse()
