"""
This module contains functions to structure the weather information into a dictionary.
"""


from typing import Dict

from utils.openweather_functools import deg_to_cardinal, build_date_timestamp, get_rain_info


def weather_data_structure(weather, city_id) -> Dict:
    """
    Structure the weather information into a dict.
    :param weather: Dictionary containing weather information.
    :param city_id: City ID.
    :return: Dictionary containing structured weather information.
    """
    return {
        'date': build_date_timestamp(timestamp=weather['dt'],
                                     timezone=weather['timezone'],
                                     mode='datetime'),
        'temp': weather['main']['temp'],
        'rainfall': get_rain_info(weather),
        'sunrise': build_date_timestamp(timestamp=weather['sys']['sunrise'],
                                        timezone=weather['timezone'],
                                        mode='hours'),
        'sunset': build_date_timestamp(timestamp=weather['sys']['sunset'],
                                       timezone=weather['timezone'],
                                       mode='hours'),
        'wind_gust_dir': deg_to_cardinal(weather['wind']['deg']),
        'wind_gust_speed': weather['wind']['speed'],
        'cloudiness': weather['clouds']['all'],
        'humidity': weather['main']['humidity'],
        'pressure': weather['main']['pressure'],
        'city_id': city_id
    }


def previous_daily_weather_data_structure(weather, city_id) -> Dict:
    """
    Structure the previous daily weather information into a dict.
    :param weather: Dictionary containing previous daily weather information.
    :param city_id: City ID.
    :return: Dictionary containing structured previous daily weather information.
    """
    return {
        'date': weather['date'],
        'min_temp': weather['temperature']['min'],
        'max_temp': weather['temperature']['max'],
        'rainfall': weather['precipitation']['total'],
        'wind_gust_dir': deg_to_cardinal(weather['wind']['max']['direction']),
        'wind_gust_speed': weather['wind']['max']['speed'],
        'cloudiness': weather['cloud_cover']['afternoon'],
        'humidity': weather['humidity']['afternoon'],
        'pressure': weather['pressure']['afternoon'],
        'city_id': city_id
    }


def previous_timestamp_weather_data_structure(weather, city_id) -> Dict:
    """
    Structure the previous timestamp weather information into a dict.
    :param weather: Dictionary containing previous timestamp weather information.
    :param city_id: City ID.
    :return: Dictionary containing structured previous timestamp weather information.
    """
    return {
        'date': build_date_timestamp(timestamp=weather['data']['dt'],
                                     timezone=weather['timezone_offset'],
                                     mode='datetime'),
        'temp': weather['data']['temp'],
        'rainfall': get_rain_info(weather['data']),
        'sunrise': build_date_timestamp(timestamp=weather['data']['sunrise'],
                                        timezone=weather['timezone_offset'],
                                        mode='hours'),
        'sunset': build_date_timestamp(timestamp=weather['data']['sunset'],
                                       timezone=weather['timezone_offset'],
                                       mode='hours'),
        'wind_gust_dir': deg_to_cardinal(weather['data']['wind_deg']),
        'wind_gust_speed': weather['data']['wind_speed'],
        'cloudiness': weather['data']['clouds'],
        'humidity': weather['data']['humidity'],
        'pressure': weather['data']['pressure'],
        'city_id': city_id
    }
