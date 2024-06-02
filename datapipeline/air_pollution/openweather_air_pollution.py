import os
from pathlib import Path

from dotenv import load_dotenv

from Extract.air_pollution.openweather_air_pollution import fetch_air_pollution
from Transform.air_pollution.openweather_air_pollution import air_pollution_data_structure
from database.mongodb_functools import MongoDBManager
from database.postgresql_functools import PostgreSQLManager, AirPollution
from utils.csv_functools import append_to_csv
from utils.json_functools import append_to_json
from utils.openweather_functools import extract_lat_lon

if __name__ == '__main__':
    load_dotenv()
    dir_path = Path(__file__).parents[2]
    verbose = True

    api_key = os.getenv('OPEN_WEATHER_API_KEY')
    locations = os.getenv('LOCATIONS').split(',')
    country_code = os.getenv('COUNTRY_CODE')

    mongo_manager = MongoDBManager()
    postgre_manager = PostgreSQLManager()

    # Extract
    cities = mongo_manager.find_documents('city', {'country': country_code})
    latitudes, longitudes = extract_lat_lon(cities, country_code)
    air_pollution = fetch_air_pollution(latitudes, longitudes, api_key)

    for air_pollution_dict in air_pollution:
        city_id = postgre_manager.fetch_city_record_by_coord(
            air_pollution_dict['coord']['lat'],
            air_pollution_dict['coord']['lon']).id

        if verbose:
            append_to_json(air_pollution_dict,
                           os.path.join(dir_path, 'dataJson', 'airPollutionInfo.json'))
        # Load
        mongo_manager.insert_document('air_pollution', air_pollution_dict)

        # Transform
        air_pollution = air_pollution_data_structure(air_pollution_dict, city_id)
        if verbose:
            append_to_csv(air_pollution, os.path.join(dir_path, 'dataCsv', 'airPollutionInfo.csv'))
        # Load
        postgre_manager.add_record(AirPollution(**air_pollution))
