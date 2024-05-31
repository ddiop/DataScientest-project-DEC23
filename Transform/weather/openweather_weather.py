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
        'Date': build_date_timestamp(timestamp=weather['dt'],
                                     timezone=weather['timezone'],
                                     mode='datetime'),
        'Temp': weather['main']['temp'],
        'Rainfall': get_rain_info(weather),
        'Sunrise': build_date_timestamp(timestamp=weather['sys']['sunrise'],
                                        timezone=weather['timezone'],
                                        mode='hours'),
        'Sunset': build_date_timestamp(timestamp=weather['sys']['sunset'],
                                       timezone=weather['timezone'],
                                       mode='hours'),
        'WindGustDir': deg_to_cardinal(weather['wind']['deg']),
        'WindGustSpeed': weather['wind']['speed'],
        'Cloudiness': weather['clouds']['all'],
        'Humidity': weather['main']['humidity'],
        'Pressure': weather['main']['pressure'],
        'City_id': city_id
    }


def previous_daily_weather_data_structure(weather, city_id) -> Dict:
    """
    Structure the previous daily weather information into a dict.
    :param weather: Dictionary containing previous daily weather information.
    :param city_id: City ID.
    :return: Dictionary containing structured previous daily weather information.
    """
    return {
        'Date': weather['date'],
        'MinTemp': weather['temperature']['min'],
        'MaxTemp': weather['temperature']['max'],
        'Rainfall': weather['precipitation']['total'],
        'WindGustDir': deg_to_cardinal(weather['wind']['max']['direction']),
        'WindGustSpeed': weather['wind']['max']['speed'],
        'Cloudiness': weather['cloud_cover']['afternoon'],
        'Humidity': weather['humidity']['afternoon'],
        'Pressure': weather['pressure']['afternoon'],
        'City_id': city_id
    }


def previous_timestamp_weather_data_structure(weather, city_id) -> Dict:
    """
    Structure the previous timestamp weather information into a dict.
    :param weather: Dictionary containing previous timestamp weather information.
    :param city_id: City ID.
    :return: Dictionary containing structured previous timestamp weather information.
    """
    return {
        'Date': build_date_timestamp(timestamp=weather['data']['dt'],
                                     timezone=weather['timezone_offset'],
                                     mode='datetime'),
        'Temp': weather['data']['temp'],
        'Rainfall': get_rain_info(weather['data']),
        'Sunrise': build_date_timestamp(timestamp=weather['data']['sunrise'],
                                        timezone=weather['timezone_offset'],
                                        mode='hours'),
        'Sunset': build_date_timestamp(timestamp=weather['data']['sunset'],
                                       timezone=weather['timezone_offset'],
                                       mode='hours'),
        'WindGustDir': deg_to_cardinal(weather['data']['wind_deg']),
        'WindGustSpeed': weather['data']['wind_speed'],
        'Cloudiness': weather['data']['clouds'],
        'Humidity': weather['data']['humidity'],
        'Pressure': weather['data']['pressure'],
        'City_id': city_id
    }
