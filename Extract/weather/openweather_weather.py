from typing import List, Dict

from utils.openweather_functools import fetch_api_data


def build_current_weather_url(latitude: float, longitude: float, api_key: str) -> str:
    """
    Constructs and returns the URL for fetching current weather information
    for a specific location from the OpenWeatherMap API.

    Documentation:
        Further details on the API endpoint can be found at:
            https://openweathermap.org/current

    :param latitude: The latitude of the location for which weather data is requested.
    :param longitude: The longitude of the location for which weather data is requested.
    :param api_key: The API key for accessing the OpenWeatherMap API.
    :return: The constructed URL for querying the current weather information.
    """
    url = "https://api.openweathermap.org/data/2.5/weather?lat=" \
          f"{latitude}&lon={longitude}&appid={api_key}&units=metric"
    return url


def build_daily_weather_url(latitude: float,
                            longitude: float,
                            date: str,
                            api_key: str) \
        -> str:
    """
    Constructs a URL for fetching historical weather data for a
    specific location and time range from the OpenWeatherMap API.

    Documentation:
        For more information on the API endpoint, visit:
            https://openweathermap.org/api/one-call-3

    :param latitude: The latitude of the location for which historical air pollution
        data is requested.
    :param longitude: The longitude of the location for which historical air pollution
        data is requested.
    :param date: The date for which the historical weather data is requested.
    :param api_key: Your API key for accessing the OpenWeatherMap API.
    :return: A URL string that can be used to query the OpenWeatherMap API for historical
        weather data.
    """
    url = "https://api.openweathermap.org/data/3.0/onecall/day_summary?lat=" \
          f"{latitude}&lon={longitude}&date={date}&appid={api_key}&units=metric"
    return url


def build_timestamp_weather_url(latitude: float,
                                longitude: float,
                                timestamp: int,
                                api_key: str) \
        -> str:
    """
    Constructs a URL for fetching historical weather data for a
    specific location and time range from the OpenWeatherMap API.

    Documentation:
        For more information on the API endpoint, visit:
            https://openweathermap.org/api/one-call-3

    :param latitude: The latitude of the location for which historical air pollution
        data is requested.
    :param longitude: The longitude of the location for which historical air pollution
        data is requested.
    :param timestamp: The start time for the historical data query, represented as a Unix timestamp.
    :param api_key: Your API key for accessing the OpenWeatherMap API.
    :return: A URL string that can be used to query the OpenWeatherMap API for historical
        weather data.
    """
    url = "https://api.openweathermap.org/data/3.0/onecall/timemachine?lat=" \
          f"{latitude}&lon={longitude}&dt={timestamp}&appid={api_key}&units=metric"
    return url


def fetch_current_weather(latitudes: List[float], longitudes: List[float], api_key: str) \
        -> List[Dict]:
    """
    Fetches weather information for a list of latitude and
    longitude pairs using the OpenWeatherMap API.

    :param latitudes: A list of latitudes for which to fetch weather information.
    :param longitudes: A list of longitudes for which to fetch weather information.
    :param api_key: The API key for accessing the OpenWeatherMap API.
    :return: A list of dictionaries, each containing the weather information for a given location.
    """
    data = []
    for lat, lon in zip(latitudes, longitudes):
        data.append(fetch_api_data(build_current_weather_url(
            lat, lon, api_key)))
    return data


def fetch_daily_weather(latitudes: List[float],
                        longitudes: List[float],
                        api_key: str,
                        date: str) \
        -> List[Dict]:
    """
    Fetches all historic weather information for a list of latitude and
    longitude pairs using the OpenWeatherMap API.

    :param latitudes: A list of latitudes for which to fetch pollution information.
    :param longitudes: A list of longitudes for which to fetch pollution information.
    :param api_key: The API key for accessing the OpenWeatherMap API.
    :param date: The date for which the historical weather data is requested.
    :return: A list of dictionaries, each containing the weather information for a given location.
    """
    data = []
    for lat, lon in zip(latitudes, longitudes):
        data.append(fetch_api_data(build_daily_weather_url(
            lat, lon, date, api_key)))
    return data


def fetch_timestamp_weather(latitudes: List[float],
                            longitudes: List[float],
                            api_key: str,
                            timestamp: int) \
        -> List[Dict]:
    """
    Fetches all historic weather information for a list of latitude and
    longitude pairs using the OpenWeatherMap API.

    :param latitudes: A list of latitudes for which to fetch pollution information.
    :param longitudes: A list of longitudes for which to fetch pollution information.
    :param api_key: The API key for accessing the OpenWeatherMap API.
    :param timestamp: The start time for the historical data query, represented as a Unix timestamp.
    :return: A list of dictionaries, each containing the weather information for a given location.
    """
    data = []
    for lat, lon in zip(latitudes, longitudes):
        data.append(fetch_api_data(build_timestamp_weather_url(
            lat, lon, timestamp, api_key)))
    return data
