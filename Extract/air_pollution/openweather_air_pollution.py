from typing import Dict, List

from utils.openweather_functools import fetch_api_data


def build_air_pollution_url(latitude: float,
                            longitude: float,
                            api_key: str) \
        -> str:
    """
    Constructs a URL for fetching current air pollution data
    for a specific location from the OpenWeatherMap API.

    Args:
        latitude (float): The latitude of the location for
            which air pollution data is requested.
        longitude (float): The longitude of the location for
            which air pollution data is requested.
        api_key (str): Your API key for accessing the OpenWeatherMap API.

    Returns:
        str: A URL string that can be used to query the OpenWeatherMap API
            for current air pollution data.

    Documentation:
        For more information on the API endpoint, visit:
            https://openweathermap.org/api/air-pollution
    """
    url = "http://api.openweathermap.org/data/2.5/air_pollution?lat=" \
          f"{latitude}&lon={longitude}&appid={api_key}"
    return url


def build_previous_air_pollution_url(latitude: float,
                                     longitude: float,
                                     start: int,
                                     end: int,
                                     api_key: str) \
        -> str:
    """
    Constructs a URL for fetching historical air pollution data for a
    specific location and time range from the OpenWeatherMap API.

    Documentation:
        For more information on the API endpoint, visit:
            https://openweathermap.org/api/air-pollution

    :arg latitude: The latitude of the location for which historical air pollution
        data is requested.
    :arg longitude: The longitude of the location for which historical air pollution
        data is requested.
    :arg start: The start time for the historical data query, represented as a Unix timestamp.
    :arg end: The end time for the historical data query, represented as a Unix timestamp.
    :arg api_key: Your API key for accessing the OpenWeatherMap API.
    :return: A URL string that can be used to query the OpenWeatherMap API for historical
        air pollution data.
    """
    url = "http://api.openweathermap.org/data/2.5/air_pollution/history?lat=" \
          f"{latitude}&lon={longitude}&start={start}&end={end}&appid={api_key}"
    return url


def fetch_air_pollution(latitudes: List[float],
                        longitudes: List[float],
                        api_key: str) \
        -> List[Dict]:
    """
    Fetches pollution information for a list of latitude and
    longitude pairs using the OpenWeatherMap API.

    :arg latitudes: A list of latitudes for which to fetch pollution information.
    :arg longitudes: A list of longitudes for which to fetch pollution information.
    :arg api_key: The API key for accessing the OpenWeatherMap API.
    :return: A list of dictionaries, each containing the pollution information for a given location.
    """
    data = []
    for lat, lon in zip(latitudes, longitudes):
        data.append(fetch_api_data(build_air_pollution_url(
            lat, lon, api_key)))
    return data


def fetch_previous_air_pollution(latitudes: List[float],
                                 longitudes: List[float],
                                 api_key: str,
                                 start: int,
                                 end: int) \
        -> List[Dict]:
    """
    Fetches all historic pollution information for a list of latitude and
    longitude pairs using the OpenWeatherMap API.

    :arg latitudes: A list of latitudes for which to fetch pollution information.
    :arg longitudes: A list of longitudes for which to fetch pollution information.
    :arg api_key: The API key for accessing the OpenWeatherMap API.
    :arg start: The start time for the historical data query, represented as a Unix timestamp.
    :arg end: The end time for the historical data query, represented as a Unix timestamp.
    :return: A list of dictionaries, each containing the pollution information for a given location.
    """
    data = []
    for lat, lon in zip(latitudes, longitudes):
        data.append(fetch_api_data(build_previous_air_pollution_url(
            lat, lon, start, end, api_key)))
    return data
