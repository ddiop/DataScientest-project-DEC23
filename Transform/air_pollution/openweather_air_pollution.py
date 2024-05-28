from typing import Dict

import pandas as pd

from utils.openweather_functools import build_date_timestamp


def air_pollution_data_structure(air_pollution, city_id) -> Dict:
    """
    Structure the air pollution information into a DataFrame.

    :arg air_pollution: Dictionary containing air pollution information.
    :arg city_id: City ID.
    :return: DataFrame containing structured air pollution information.
    """
    return {
        'Date': build_date_timestamp(air_pollution['list'][0]['dt'],
                                     mode='datetime'),
        'AirQualityIndex': air_pollution['list'][0]['main']['aqi'],
        'COConcentration': air_pollution['list'][0]['components']['co'],
        'NOConcentration': air_pollution['list'][0]['components']['no'],
        'NO2Concentration': air_pollution['list'][0]['components']['no2'],
        'O3Concentration': air_pollution['list'][0]['components']['o3'],
        'SO2Concentration': air_pollution['list'][0]['components']['so2'],
        'PM25Concentration': air_pollution['list'][0]['components']['pm2_5'],
        'PM10Concentration': air_pollution['list'][0]['components']['pm10'],
        'NH3Concentration': air_pollution['list'][0]['components']['nh3'],
        'City_id': city_id
    }


def previous_air_pollution_data_structure(air_pollution, city_id) -> pd.DataFrame:
    """
    Structure the air pollution information into a DataFrame.

    :arg air_pollution: Dictionary containing air pollution information.
    :arg city_id: City ID.
    :return: DataFrame containing structured air pollution information.
    """
    structured_data = []
    for i in range(len(air_pollution['list'])):
        structured_data.append({
            'Date': build_date_timestamp(air_pollution['list'][i]['dt'],
                                         mode='datetime'),
            'AirQualityIndex': air_pollution['list'][i]['main']['aqi'],
            'COConcentration': air_pollution['list'][i]['components']['co'],
            'NOConcentration': air_pollution['list'][i]['components']['no'],
            'NO2Concentration': air_pollution['list'][i]['components']['no2'],
            'O3Concentration': air_pollution['list'][i]['components']['o3'],
            'SO2Concentration': air_pollution['list'][i]['components']['so2'],
            'PM25Concentration': air_pollution['list'][i]['components']['pm2_5'],
            'PM10Concentration': air_pollution['list'][i]['components']['pm10'],
            'NH3Concentration': air_pollution['list'][i]['components']['nh3'],
            'City_id': city_id
            })
    return pd.DataFrame(structured_data)
