from typing import Dict

import pandas as pd

from utils.openweather_functools import build_date_timestamp


def air_pollution_data_structure(air_pollution, city_id) -> Dict:
    """
    Structure the air pollution information into a DataFrame.

    :param air_pollution: Dictionary containing air pollution information.
    :param city_id: City ID.
    :return: DataFrame containing structured air pollution information.
    """
    return {
        'date': build_date_timestamp(air_pollution['list'][0]['dt'],
                                     mode='datetime'),
        'air_quality_index': air_pollution['list'][0]['main']['aqi'],
        'co_concentration': air_pollution['list'][0]['components']['co'],
        'no_concentration': air_pollution['list'][0]['components']['no'],
        'no2_concentration': air_pollution['list'][0]['components']['no2'],
        'o3_concentration': air_pollution['list'][0]['components']['o3'],
        'so2_concentration': air_pollution['list'][0]['components']['so2'],
        'pm25_concentration': air_pollution['list'][0]['components']['pm2_5'],
        'pm10_concentration': air_pollution['list'][0]['components']['pm10'],
        'nh3_concentration': air_pollution['list'][0]['components']['nh3'],
        'city_id': city_id
    }


def previous_air_pollution_data_structure(air_pollution, city_id) -> pd.DataFrame:
    """
    Structure the air pollution information into a DataFrame.

    :param air_pollution: Dictionary containing air pollution information.
    :param city_id: City ID.
    :return: DataFrame containing structured air pollution information.
    """
    structured_data = []
    for i in range(len(air_pollution['list'])):
        structured_data.append({
            'date': build_date_timestamp(air_pollution['list'][i]['dt'],
                                         mode='datetime'),
            'air_quality_index': air_pollution['list'][i]['main']['aqi'],
            'co_concentration': air_pollution['list'][i]['components']['co'],
            'no_concentration': air_pollution['list'][i]['components']['no'],
            'no2_concentration': air_pollution['list'][i]['components']['no2'],
            'o3_concentration': air_pollution['list'][i]['components']['o3'],
            'so2_concentration': air_pollution['list'][i]['components']['so2'],
            'pm25_concentration': air_pollution['list'][i]['components']['pm2_5'],
            'pm10_concentration': air_pollution['list'][i]['components']['pm10'],
            'nh3_concentration': air_pollution['list'][i]['components']['nh3'],
            'city_id': city_id
            })
    return pd.DataFrame(structured_data)
