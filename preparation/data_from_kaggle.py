import os
from pathlib import Path

import numpy as np
import pandas as pd
from dotenv import load_dotenv

from database.postgresql_functools import PostgresManager
from utils.json_functools import load_from_json


def load_kaggle(locations, path, postgres):
    pd.read_csv(os.path.join(path, 'data', 'csv', 'weatherAUS.csv')) \
        .drop(columns=['RainToday', 'RainTomorrow']) \
        .rename(columns={'Date': 'date',
                         'Location': 'location',
                         'MinTemp': 'min_temp',
                         'MaxTemp': 'max_temp',
                         'Rainfall': 'rainfall',
                         'Evaporation': 'evaporation',
                         'Sunshine': 'sunshine',
                         'WindGustDir': 'wind_gust_dir',
                         'WindGustSpeed': 'wind_gust_speed',
                         'WindDir9am': 'wind_dir_9am',
                         'WindDir3pm': 'wind_dir_3pm',
                         'WindSpeed9am': 'wind_speed_9am',
                         'WindSpeed3pm': 'wind_speed_3pm',
                         'Humidity9am': 'humidity_9am',
                         'Humidity3pm': 'humidity_3pm',
                         'Pressure9am': 'pressure_9am',
                         'Pressure3pm': 'pressure_3pm',
                         'Cloud9am': 'cloud_9am',
                         'Cloud3pm': 'cloud_3pm',
                         'Temp9am': 'temp_9am',
                         'Temp3pm': 'temp_3pm'}) \
        .replace('NA', np.nan) \
        .loc[lambda x: x['location'].isin(locations)] \
        .to_sql('australian_meteorology_weather', postgres.engine,
                if_exists='append', index=False)


if __name__ == '__main__':
    dir_path = Path(__file__).parents[1]
    load_dotenv()
    config = load_from_json(os.path.join(dir_path, 'config.json'))
    locations_to_keep = config['locations']
    postgres_manager = PostgresManager()

    load_kaggle(locations_to_keep, dir_path, postgres_manager)
