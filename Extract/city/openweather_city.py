def build_city_url(city_name: str, api_key: str) -> str:
    """
    Constructs and returns the URL for fetching city
    information from the OpenWeatherMap API.

    Documentation:
        Further details on the API endpoint can be found at:
            https://openweathermap.org/api/geocoding-api

    :arg city_name: The name of the city.
    :arg api_key: The API key for accessing the OpenWeatherMap API.
    :return: The constructed URL for the city information request.
    """
    url = "http://api.openweathermap.org/geo/1.0/direct?q=" \
          f"{city_name}&limit=1&appid={api_key}"
    return url
