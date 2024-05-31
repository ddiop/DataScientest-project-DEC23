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
        'Name': city_info['name'],
        'Country': city_info['country'],
        'Latitude': city_info['lat'],
        'Longitude': city_info['lon']
    }
