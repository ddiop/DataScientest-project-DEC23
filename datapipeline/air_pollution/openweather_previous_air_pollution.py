import os

from dotenv import load_dotenv

from Extract.air_pollution.openweather_air_pollution import fetch_previous_air_pollution
from Transform.air_pollution.openweather_air_pollution import previous_air_pollution_data_structure
from database.mongodb_functools import MongoDBManager
from database.postgresql_functools import PostgreSQLManager, AirPollution
from utils.json_functools import append_to_json
from utils.csv_functools import append_to_csv
from utils.openweather_functools import extract_lat_lon


if __name__ == '__main__':
    load_dotenv()
    verbose = True

    api_key = os.getenv('OPEN_WEATHER_API_KEY')
    locations = os.getenv('LOCATIONS').split(',')
    country_code = os.getenv('COUNTRY_CODE')

    mongo_manager = MongoDBManager()
    postgre_manager = PostgreSQLManager()

    # Extract
    cities = mongo_manager.find_documents('City', {'country': country_code})
    latitudes, longitudes = extract_lat_lon(cities, country_code)
    air_pollution = fetch_previous_air_pollution(latitudes, longitudes, api_key,
                                                 start=1606435200, end=1709485840)

    for air_pollution_dict in air_pollution:
        city_id = postgre_manager.fetch_city_record_by_coord(
            air_pollution_dict['coord']['lat'],
            air_pollution_dict['coord']['lon']).id

        if verbose:
            append_to_json(air_pollution_dict, os.path.join('json', 'AirPollutionInfo.json'))
        # Load
        mongo_manager.insert_document('AirPollution', air_pollution_dict)

        # Transform
        air_pollution_df = previous_air_pollution_data_structure(air_pollution_dict, city_id)
        # Load
        for i in range(len(air_pollution_df)):
            if verbose:
                append_to_csv(data=air_pollution_df.to_dict('records')[i], filename=os.path.join('csv', 'AirPollutionInfo.csv'))
            postgre_manager.add_record(AirPollution(**air_pollution_df.to_dict('records')[i]))
