"""
This module contains functions to transform the OpenWeather city data
"""


from typing import Dict


def city_data_structure(city_info) -> Dict:
    """
    Structure the city information into a DataFrame.

    :param city_info: Dictionary containing city information.
    :return: DataFrame containing structured city information.
    """
    return {
        'name': city_info['name'],
        'country': city_info['country'],
        'latitude': city_info['lat'],
        'longitude': city_info['lon']
    }
