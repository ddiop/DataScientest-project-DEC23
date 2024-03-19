"""
OpenWeather API tools.
"""

from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional

import json
import requests
import yaml


def load_config(config_file: str = 'config.yml') -> Dict:
    """
    Loads YAML configuration and returns it as a dictionary.

    Args:
        config_file (str): Path to the YAML file containing configuration data.

    Returns:
        Dict: A dictionary containing configuration parameters.
    """
    with open(config_file, 'r', encoding='utf-8') as file:
        config_data = yaml.safe_load(file)
    return config_data


def store_to_json(data: Dict, filename: str = 'example.json') -> None:
    """
    Saves a dictionary to a JSON file with pretty formatting.

    Args:
        data (Dict): Dictionary containing data to be saved.
        filename (str): Name of the file to save the data in.
    """
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)


def load_from_json(filename: str = 'example.json') -> Dict:
    """
    Loads data from a JSON file and returns it as a dictionary.

    Args:
        filename (str): Name of the file to load the data from.

    Returns:
        Dict: A dictionary containing the loaded data.
    """
    with open(filename, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data


def build_date_timestamp(
        timestamp: int, timezone: int = 0, mode: str = 'date') -> str:
    """
    Converts a UNIX timestamp to a formatted date or
    time string based on timezone and mode.

    Args:
        timestamp (int): UNIX timestamp.
        timezone (int): Timezone offset in seconds.
        mode (str): 'date' for date string, 'hours' for time string.

    Returns:
        str: Formatted date or time string.

    Raises:
        NotImplementedError: If mode is not 'date' or 'hours'
    """
    # Convert timestamp to UTC datetime
    utc_time = datetime.utcfromtimestamp(timestamp)
    # Create timedelta object for timezone offset
    timezone_offset = timedelta(seconds=timezone)
    # Apply timezone offset to UTC time
    local_time = utc_time + timezone_offset

    # Return formatted date or time based on mode
    if mode == 'date':
        return local_time.strftime('%Y-%m-%d')
    if mode == 'hours':
        return local_time.strftime('%H:%M:%S')
    raise NotImplementedError


def deg_to_cardinal(deg: float) -> str:
    """
    Converts a degree to its corresponding cardinal direction.

    Args:
        deg (float): Degree to be converted.

    Returns:
        str: A string representing the cardinal direction.
    """
    directions = [
        'N', 'NNE', 'NE', 'ENE',
        'E', 'ESE', 'SE', 'SSE',
        'S', 'SSW', 'SW', 'WSW',
        'W', 'WNW', 'NW', 'NNW', 'N'
    ]
    # Calculate index for the directions list
    index = int((deg + 11.25) % 360 / 22.5)
    return directions[index]  # Return the corresponding cardinal direction


def get_rain_info(data: Optional[Dict[str, Dict[str, float]]] = None) -> float:
    """
    Extracts 1-hour rain volume information from data, if available.

    Args:
        data (Optional[Dict[str, Dict[str, float]]]): Optional
            dictionary containing weather data,
            including rain information structured as {'rain': {'1h': float}}.
            Defaults to None.

    Returns:
        float: The volume of rain in the last 1 hour in millimeters.
            Returns 0.0 if data is unavailable or does not contain the
            required information.
    """
    # Check if data is None and initialize it to a default value if so
    if data is None:
        data = {'rain': {'1h': 0.0}}
    # Safely extract and return the rain volume,
    # defaulting to 0.0 if not present
    return float(data.get('rain', {}).get('1h', 0.0))


def build_city_info_url(city_name: str, limit: int, api_key: str) -> str:
    """
    Constructs and returns the URL for fetching city
    information from the OpenWeatherMap API.
    doc: https://openweathermap.org/api/geocoding-api

    Args:
        city_name (str): The name of the city.
        limit (int): The limit for the number of search results.
        api_key (str): The API key for accessing the OpenWeatherMap API.
    
    Returns:
        url (str): The constructed URL for the city information request.
    """
    url = "http://api.openweathermap.org/geo/1.0/direct?q=" \
          f"{city_name}&limit={limit}&appid={api_key}"
    return url


def build_weather_info_url(
        latitude: float, longitude: float, api_key: str) -> str:
    """
    Constructs and returns the URL for fetching current weather information
    for a specific location from the OpenWeatherMap API.

    Args:
        latitude (float): The latitude of the location for
            which weather data is requested.
        longitude (float): The longitude of the location for
            which weather data is requested.
        api_key (str): The API key for accessing the OpenWeatherMap API.

    Returns:
        str: The constructed URL for querying the current weather information.

    Documentation:
        Further details on the API endpoint can be found at:
            https://openweathermap.org/current
    """
    url = "https://api.openweathermap.org/data/2.5/weather?lat=" \
          f"{latitude}&lon={longitude}&appid={api_key}&units=metric"
    return url


def build_pollution_info_url(
        latitude: float, longitude: float, api_key: str) -> str:
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


def build_previous_pollution_info_url(
        latitude: float,
        longitude: float,
        start: int,
        end: int,
        api_key: str
        ) -> str:
    """
    Constructs a URL for fetching historical air pollution data for a
    specific location and time range from the OpenWeatherMap API.

    Args:
        latitude (float): The latitude of the location for
            which historical air pollution data is requested.
        longitude (float): The longitude of the location for
            which historical air pollution data is requested.
        start (int): The start time for the historical data query,
            represented as a Unix timestamp.
        end (int): The end time for the historical data query,
            represented as a Unix timestamp.
        api_key (str): Your API key for accessing the OpenWeatherMap API.

    Returns:
        str: A URL string that can be used to query the OpenWeatherMap API
            for historical air pollution data.

    Documentation:
        For more information on the API endpoint, visit:
            https://openweathermap.org/api/air-pollution
    """
    url = "http://api.openweathermap.org/data/2.5/air_pollution/history?lat=" \
          f"{latitude}&lon={longitude}&start={start}&end={end}&appid={api_key}"
    return url


def fetch_api_data(url: str) -> Dict:
    """
    Fetches data from the given API URL and returns it as a dictionary.
    Raises an exception for non-200 responses.

    Args:
        url (str): The URL from which to fetch the data.

    Returns:
        data (Dict): The data retrieved from the API,
            parsed into a dictionary.

    Raises:
        ConnectionError: If the API response status code is not 200.
    """
    response = requests.get(url, timeout=10)
    if response.status_code == 200:
        data = response.json()
        return data
    raise ConnectionError(f"Web server response: {response.status_code}")


def extract_lat_lon(
        data: List[Dict], country_code: str) -> Tuple[List[float], List[float]]:
    """
    Extracts latitudes and longitudes for locations within
    the specified country from the provided dataset.

    Args:
        data (List[Dict]): A list of dictionaries, each representing
            a location. Each dictionary contains keys for 'lat' (latitude),
            'lon' (longitude), and 'country' (country code).
        Country_code (str): The ISO 3166-1 alpha-2 country code
            used to filter locations by country.

    Returns:
        latitudes, longitudes (Tuple[List[float], List[float]]):
            A tuple containing two lists:
            * The first list contains the latitudes of
                locations within the specified country.
            * The second list contains the longitudes of these locations.
    """
    latitudes, longitudes = [], []
    for location in data:
        if location['country'] == country_code:
            latitudes.append(location['lat'])
            longitudes.append(location['lon'])
    return latitudes, longitudes


def fetch_weather_info_for_coordinates(
        latitudes: List[float],
        longitudes: List[float],
        api_key: str
        ) -> List[Dict]:
    """
    Fetches weather information for a list of latitude and
    longitude pairs using the OpenWeatherMap API.

    Args:
        latitudes (List[float]): A list of latitudes for which
            to fetch weather information.
        longitudes (List[float]): A list of longitudes for which
            to fetch weather information.
        api_key (str): The API key for accessing the OpenWeatherMap API.

    Returns:
        weather_data (List[Dict]): A list of dictionaries, each containing
            the weather information for a given location.
    """
    data = []
    for lat, lon in zip(latitudes, longitudes):
        data.append(fetch_api_data(build_weather_info_url(
            lat, lon, api_key)))
    return data


def fetch_pollution_info_for_coordinates(
        latitudes: List[float],
        longitudes: List[float],
        api_key: str
        ) -> List[Dict]:
    """
    Fetches pollution information for a list of latitude and
    longitude pairs using the OpenWeatherMap API.

    Args:
        latitudes (List[float]): A list of latitudes for which
            to fetch pollution information.
        longitudes (List[float]): A list of longitudes for which
            to fetch pollution information.
        api_key (str): The API key for accessing the OpenWeatherMap API.

    Returns:
        pollution_data (List[Dict]): A list of dictionaries, each containing
            the pollution information for a given location.
    """
    data = []
    for lat, lon in zip(latitudes, longitudes):
        data.append(fetch_api_data(build_pollution_info_url(
            lat, lon, api_key)))
    return data


def fetch_historic_pollution(
        latitudes: List[float],
        longitudes: List[float],
        api_key: str,
        start: int,
        end: int
        ) -> List[Dict]:
    """
    Fetches all historic pollution information for a list of latitude and
    longitude pairs using the OpenWeatherMap API.

    Args:
        latitudes (List[float]): A list of latitudes for which
            to fetch pollution information.
        longitudes (List[float]): A list of longitudes for which
            to fetch pollution information.
        api_key (str): The API key for accessing the OpenWeatherMap API.
        start (int): The start time for the historical data query,
            represented as a Unix timestamp.
        end (int): The end time for the historical data query,
            represented as a Unix timestamp.

    Returns:
        pollution_data (List[Dict]): A list of dictionaries, each containing
            the pollution information for a given location.
    """
    data = []
    for lat, lon in zip(latitudes, longitudes):
        data.append(fetch_api_data(build_previous_pollution_info_url(
            lat, lon, start, end, api_key)))
    return data
