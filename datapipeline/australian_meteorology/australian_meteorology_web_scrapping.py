"""
This script is used to scrape the Australian Bureau of Meteorology website
"""


import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv

from Extract.australian_meteorology.australian_meteorology_extract import generate_urls
from Transform.australian_meteorology.australian_meteorology_transform import aggregate_weather_data
from database.postgresql_functools import PostgreSQLManager, AustralianMeteorologyWeather

if __name__ == '__main__':
    load_dotenv()
    dir_path = Path(__file__).parents[2]
    verbose = True

    # Define the dates to scrape: <year><month>
    dates_to_scrape = ['202304', '202305', '202306', '202307', '202308', '202309',
                       '202310', '202311', '202312', '202401', '202402', '202403',
                       '202404', '202405']

    # Define the locations to scrape: <location>: <location_id_on_website>
    locations_to_scrape = {'Canberra': '2801',
                           'Tuggeranong': '2802',
                           'Mount Ginini': '2804'}

    # Generate the URLs to scrape
    pages_to_scrape = generate_urls(dates_to_scrape, list(locations_to_scrape.values()))

    # Aggregate the weather data
    weather_df = aggregate_weather_data(pages_to_scrape)
    for col in ['wind_gust_dir', 'wind_dir_9am', 'wind_dir_3pm']:
        weather_df[col] = weather_df[col].replace({-1: 'NA'})

    # Store the weather data to PostgreSQL database
    postgre_manager = PostgreSQLManager()
    for i in range(len(weather_df)):
        australian_weather = AustralianMeteorologyWeather(**weather_df.to_dict('records')[i])
        postgre_manager.add_record(australian_weather)

    # Save the weather data to a CSV file
    if verbose:
        if os.path.exists(
                os.path.join(dir_path, 'dataCsv', 'australianMeteorologyWeatherInfo.csv')):
            df_tmp = pd.read_csv(
                os.path.join(dir_path, 'dataCsv', 'australianMeteorologyWeatherInfo.csv'))
            weather_df = pd.concat([df_tmp, weather_df], ignore_index=True)
        weather_df.to_csv(os.path.join(dir_path, 'dataCsv', 'australianMeteorologyWeatherInfo.csv'),
                          index=False)
