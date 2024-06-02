import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv

from database.postgresql_functools import PostgreSQLManager, AustralianMeteorologyWeather
from utils.csv_functools import append_to_csv

load_dotenv()
verbose = True
dir_path = Path().resolve().parent

postgres = PostgreSQLManager()

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
print(df_daily)
df_daily = df_daily.drop_duplicates(subset=['date', 'location'])
df_daily['evaporation'], df_daily['sunshine'] = -1, -1

weather_9am_query = """
SELECT 
    EXTRACT(YEAR FROM w.date) || '-' || EXTRACT(MONTH FROM w.date) || '-' || EXTRACT(DAY FROM w.date) AS date,
    c.name AS location,
    w.temp,
    w.cloud,
    w.pressure,
    w.humidity,
    w.wind_gust_speed,
    w.wind_gust_dir
FROM 
    weather w
JOIN 
    city c ON w.city_id = c.id
WHERE 
    EXTRACT(HOUR FROM w.date) = 17
ORDER BY 
    c.name, w.date
"""

weather_3pm_query = """
SELECT 
    EXTRACT(YEAR FROM w.date) || '-' || EXTRACT(MONTH FROM w.date) || '-' || EXTRACT(DAY FROM w.date) AS date,
    c.name AS location,
    w.temp,
    w.cloud,
    w.pressure,
    w.humidity,
    w.wind_gust_speed,
    w.wind_gust_dir
FROM 
    weather w
JOIN 
    city c ON w.city_id = c.id
WHERE 
    EXTRACT(HOUR FROM w.date) = 23
ORDER BY 
    c.name, w.date
"""

df_9am = pd.read_sql_query(weather_9am_query, postgres.engine)
df_9am = df_9am.drop_duplicates(subset=['date', 'location'])

df_3pm = pd.read_sql_query(weather_3pm_query, postgres.engine)
df_3pm = df_3pm.drop_duplicates(subset=['date', 'location'])

df_3_9 = pd.merge(df_9am, df_3pm, on=['date', 'location'], suffixes=("_9am", "_3pm"))

df_open = pd.merge(df_daily, df_3_9, on=['date', 'location'])

for i in range(len(df_open)):
    if verbose:
        append_to_csv(data=df_open.to_dict('records')[i],
                      filename=os.path.join(dir_path, 'dataCsv',
                                            'australianMeteorologyWeatherInfo.csv'))
    postgres.add_record(AustralianMeteorologyWeather(**df_open.to_dict('records')[i]))
