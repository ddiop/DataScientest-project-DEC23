import requests
import json
import yaml

from datetime import datetime, timedelta
from typing import List, Tuple, Dict, Optional


def load_config(config_file: str = 'config.yml') -> Dict:
    """
    Loads and returns the configuration from a YAML file.
    
    Parameters:
        - config_file (str): The path to the YAML configuration file.
    
    Returns:
        - config_data (dict): The configuration data as a dictionary.
    """
    with open(config_file, 'r') as file:
        config_data = yaml.safe_load(file)
    return config_data
    
def store_to_json(data: dict, filename: str = 'example.json') -> None:
    """
    Stores a dictionary to a JSON file.
    
    Parameters:
        - data (dict): The data to be stored in the JSON file.
        - filename (str): The name of the JSON file where the data will be stored.
    """
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)
    
def load_from_json(filename: str = 'example.json') -> Dict:
    """
    Loads data from a JSON file and returns it as a dictionary.
    
    Parameters:
        - filename (str): The name of the JSON file to load the data from.
    
    Returns:
        - data (dict): The data loaded from the JSON file.
    """
    with open(filename, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

def build_date_timestamp(timestamp, timezone=0, mode='date'):
    utc_time = datetime.utcfromtimestamp(timestamp)
    timezone_offset = timedelta(seconds=timezone)
    local_time = utc_time + timezone_offset

    if mode == 'date':
        date_formated = local_time.strftime('%Y-%m-%d')
        return date_formated
    elif mode == 'hours':
        hours_formatee = local_time.strftime('%H:%M:%S')
        return hours_formatee
    else:
        raise NotImplementedError
    
def deg_to_cardinal(deg):
    directions = [
        'N', 'NNE', 'NE', 'ENE',
        'E', 'ESE', 'SE', 'SSE',
        'S', 'SSW', 'SW', 'WSW',
        'W', 'WNW', 'NW', 'NNW', 'N'
    ]
    cardinal = directions[int((deg + 11.25) % 360 / 22.5)]
    return cardinal

def get_rain_info(data):
    data_rain = data.get('rain', {})
    data_rain_1h = data_rain.get('1h', 'NA')
    return data_rain_1h

def build_city_info_url(city_name: str, limit: int, api_key: str) -> str:
    """
    Constructs and returns the URL for fetching city information from the OpenWeatherMap API.
    doc: https://openweathermap.org/api/geocoding-api

    Parameters:
        - city_name (str): The name of the city.
        - limit (int): The limit for the number of search results.
        - api_key (str): The API key for accessing the OpenWeatherMap API.
    
    Returns:
        - url (str): The constructed URL for the city information request.
    """
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit={limit}&appid={api_key}"
    return url

def build_weather_info_url(latitude: float, longitude: float, api_key: str) -> str:
    """
    Constructs and returns the URL for fetching weather information from the OpenWeatherMap API.
    doc: https://openweathermap.org/current
    
    Parameters:
        - latitude (float): The latitude of the location.
        - longitude (float): The longitude of the location.
        - api_key (str): The API key for accessing the OpenWeatherMap API.
    
    Returns:
        - url (str): The constructed URL for the weather information request.
    """
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={api_key}&units=metric"
    return url

def build_pollution_info_url(latitude: float, longitude: float, api_key: str) -> str:
    """doc: https://openweathermap.org/api/air-pollution"""
    url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={latitude}&lon={longitude}&appid={api_key}"
    return url

def build_previous_pollution_info_url(latitude: float, longitude: float, start, end, api_key: str) -> str:
    """doc: https://openweathermap.org/api/air-pollution"""
    url = f"http://api.openweathermap.org/data/2.5/air_pollution/history?lat={latitude}&lon={longitude}&start={start}&end={end}&appid={api_key}"
    return url


def fetch_api_data(url: str) -> Dict:
    """
    Fetches data from the given API URL and returns it as a dictionary. Raises an exception for non-200 responses.
    
    Parameters:
        - url (str): The URL from which to fetch the data.
    
    Returns:
        - data (Dict): The data retrieved from the API, parsed into a dictionary.
    
    Raises:
        - ConnectionError: If the API response status code is not 200.
    """
    response = requests.get(url)
    if response.status_code == 200: 
        data = response.json()
        return data
    else:
        raise ConnectionError(f"Web server response: {response.status_code}")


def extract_lat_lon(data: List[Dict], country_code: str) -> Tuple[List[float], List[float]]:
    """
    Extracts latitudes and longitudes for locations within the specified country from the provided dataset.

    Parameters:
        - data (List[Dict]): A list of dictionaries, each representing a location. Each dictionary contains 
                           keys for 'lat' (latitude), 'lon' (longitude), and 'country' (country code).
        - country_code (str): The ISO 3166-1 alpha-2 country code used to filter locations by country.

    Returns:
        - latitudes, longitudes (Tuple[List[float], List[float]]): A tuple containing two lists:
            * The first list contains the latitudes of locations within the specified country.
            * The second list contains the longitudes of these locations.
    """
    latitudes = [location['lat'] for location in data if location['country'] == country_code]
    longitudes = [location['lon'] for location in data if location['country'] == country_code]
    return latitudes, longitudes


def fetch_weather_info_for_coordinates(mode, latitudes: List[float], longitudes: List[float], api_key: str, start: Optional[int] = None, end: Optional[int] = None) -> List[Dict]:
    """
    Fetches weather information for a list of latitude and longitude pairs using the OpenWeatherMap API.
    
    Parameters:
        - latitudes (List[float]): A list of latitudes for which to fetch weather information.
        - longitudes (List[float]): A list of longitudes for which to fetch weather information.
        - api_key (str): The API key for accessing the OpenWeatherMap API.
    
    Returns:
        - weather_data (List[Dict]): A list of dictionaries, each containing the weather information for a given location.
    """
    if mode == 'weather':
        data = [fetch_api_data(build_weather_info_url(lat, lon, api_key)) for lat, lon in zip(latitudes, longitudes)]
        return data
    elif mode == 'air_pollution':
        data = [fetch_api_data(build_pollution_info_url(lat, lon, api_key)) for lat, lon in zip(latitudes, longitudes)]
        return data
    elif mode == 'previous_air_pollution':
        data = [fetch_api_data(build_previous_pollution_info_url(lat, lon, start, end, api_key)) for lat, lon in zip(latitudes, longitudes)]
        return data
    else:
        raise NotImplementedError
