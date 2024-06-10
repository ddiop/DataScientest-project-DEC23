import json
import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv

from database.mongodb_functools import MongoDBManager
from database.postgresql_functools import PostgresManager, Weather, DailyWeather
from utils.openweather_functools import deg_to_cardinal, build_date_timestamp, get_rain_info


def load_daily_weather(path, postgre, mongo):
    with open(os.path.join(path, 'data', 'json', 'dataDailyAggregation.json'), 'r') as f:
        for line in f:
            data = json.loads(line)

            mongo.insert_document('weather', data)

            city_id = postgre.fetch_city_record_by_coord(
                data['lat'],
                data['lon']).id

            weather = {'date': data['date'],
                       'min_temp': data['temperature']['min'],
                       'max_temp': data['temperature']['max'],
                       'rainfall': data['precipitation']['total'],
                       'wind_gust_dir': deg_to_cardinal(data['wind']['max']['direction']),
                       'wind_gust_speed': data['wind']['max']['speed'],
                       'cloud': data['cloud_cover']['afternoon'],
                       'humidity': data['humidity']['afternoon'],
                       'pressure': data['pressure']['afternoon'],
                       'city_id': city_id
                       }
            postgre.add_record(DailyWeather(**weather))


def load_timestamp_weather(path, postgre, mongo):
    with open(os.path.join(path, 'data', 'json', 'dataWeatherTimeStamp.json'), 'r') as f:
        for line in f:
            data = json.loads(line)

            mongo.insert_document('weather', data)

            city_id = postgre.fetch_city_record_by_coord(
                data['lat'],
                data['lon']).id

            weather = {'date': build_date_timestamp(timestamp=data['data'][0]['dt'],
                                                    timezone=data['timezone_offset'],
                                                    mode='datetime'),
                       'temp': data['data'][0]['temp'],
                       'rainfall': get_rain_info(data['data'][0]),
                       'sunrise': build_date_timestamp(timestamp=data['data'][0]['sunrise'],
                                                       timezone=data['timezone_offset'],
                                                       mode='hours'),
                       'sunset': build_date_timestamp(timestamp=data['data'][0]['sunset'],
                                                      timezone=data['timezone_offset'],
                                                      mode='hours'),
                       'wind_dir': deg_to_cardinal(data['data'][0]['wind_deg']),
                       'wind_speed': data['data'][0]['wind_speed'],
                       'cloud': data['data'][0]['clouds'],
                       'humidity': data['data'][0]['humidity'],
                       'pressure': data['data'][0]['pressure'],
                       'city_id': city_id
                       }
            postgre.add_record(Weather(**weather))


def get_daily_weather_data(postgres):
    daily_weather_query = """
    SELECT
        EXTRACT(YEAR FROM dw.date) || '-' || EXTRACT(MONTH FROM dw.date) || '-' || EXTRACT(DAY FROM dw.date) AS date,
        c.name AS location,
        dw.min_temp,
        dw.max_temp,
        dw.rainfall,
        dw.wind_gust_speed,
        dw.wind_gust_dir
    FROM
        daily_weather dw
    JOIN
        city c ON dw.city_id = c.id
    ORDER BY
        c.name, dw.date
    """
    df_daily = pd.read_sql_query(daily_weather_query, postgres.engine)
    df_daily['evaporation'], df_daily['sunshine'] = -1, -1
    return df_daily


def get_weather_9am_data(postgres):
    weather_9am_query = """
    SELECT
        EXTRACT(YEAR FROM w.date) || '-' || EXTRACT(MONTH FROM w.date) || '-' || EXTRACT(DAY FROM w.date) AS date,
        c.name AS location,
        w.temp,
        w.cloud,
        w.pressure,
        w.humidity,
        w.wind_speed,
        w.wind_dir
    FROM
        weather w
    JOIN
        city c ON w.city_id = c.id
    WHERE
        EXTRACT(HOUR FROM w.date) = 17  -- TODO be careful 9am w/o timezone offset
    ORDER BY
        c.name, w.date
    """
    df_9am = pd.read_sql_query(weather_9am_query, postgres.engine)
    return df_9am


def get_weather_3pm_data(postgres):
    weather_3pm_query = """
    SELECT
        EXTRACT(YEAR FROM w.date) || '-' || EXTRACT(MONTH FROM w.date) || '-' || EXTRACT(DAY FROM w.date) AS date,
        c.name AS location,
        w.temp,
        w.cloud,
        w.pressure,
        w.humidity,
        w.wind_speed,
        w.wind_dir
    FROM
        weather w
    JOIN
        city c ON w.city_id = c.id
    WHERE
        EXTRACT(HOUR FROM w.date) = 23  -- TODO be careful 3pm w/o timezone offset
    ORDER BY
        c.name, w.date
    """
    df_3pm = pd.read_sql_query(weather_3pm_query, postgres.engine)
    return df_3pm


def load_kaggle_format_weather(postgres):
    df_daily = get_daily_weather_data(postgres)
    df_9am = get_weather_9am_data(postgres)
    df_3pm = get_weather_3pm_data(postgres)

    df_3_9 = pd.merge(df_9am, df_3pm, on=['date', 'location'], suffixes=("_9am", "_3pm"))
    df_open = pd.merge(df_daily, df_3_9, on=['date', 'location'])

    df_open.to_sql('australian_meteorology_weather',
                   postgres.engine, if_exists='append', index=False)


if __name__ == '__main__':
    dir_path = Path(__file__).parents[1]
    load_dotenv()
    mongo_manager = MongoDBManager()
    postgres_manager = PostgresManager()

    load_daily_weather(dir_path, postgres_manager, mongo_manager)
    load_timestamp_weather(dir_path, postgres_manager, mongo_manager)
    load_kaggle_format_weather(postgres_manager)
