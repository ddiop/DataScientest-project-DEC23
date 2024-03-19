"""
Web scrapping Australian Bureau of Meteorology.
"""

from datetime import datetime
from itertools import product
import re
from typing import List, Optional, Tuple

from bs4 import BeautifulSoup
import pandas as pd
import requests


def generate_urls(dates: List[str], locations: List[str]) -> List[str]:
    """
    Generates URLs for weather data based on specified dates and locations.

    Args:
        dates (List[str]): List of dates for which to fetch weather data.
        locations (List[str]): List of location codes to
        fetch weather data for.

    Returns:
        List[str]: List of URLs constructed based on the
        specified dates and locations.
    """
    # Base URL for the Australian Bureau of Meteorology website's weather data
    base_url = ("https://reg.bom.gov.au/climate/dwo/{date}/"
                "html/IDCJDW{location}.{date}.shtml")
    # Create URLs for all combinations of dates and locations
    return [base_url.format(date=date, location=location)
            for date, location in product(dates, locations)]


def fetch_page_content(url: str) -> Optional[BeautifulSoup]:
    """
    Fetches the HTML content from a given URL.

    Args:
        url (str): The URL from which to fetch the content.

    Returns:
        Optional[BeautifulSoup]: BeautifulSoup object containing the
        parsed HTML content, or None if the request fails.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise an exception for bad responses
        # Parse and return the HTML content
        bs = BeautifulSoup(response.content, 'lxml')
        return bs
    except requests.RequestException as e:
        # Print the error if request fails
        print(f"Error fetching URL {url}: {e}")
        return None


def extract_simplified_information(
        html: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Extracts simplified location and date information from the HTML
    content of a page.

    Args:
        html (str): HTML content as a string.

    Returns:
        Tuple[Optional[str], Optional[str]]: A tuple containing the
        location and date, or None if not found.
    """
    # Use regular expression to extract location and date in the HTML content
    match = re.search(r"<h1>(?P<location>.+?)(?:<br/?>|,)\s*"
                      r"(?P<date>\w+ \d{4})", html, re.IGNORECASE)
    if match:
        # Extract location
        location = match.group('location').split(',')[0].strip()
        # Extract date
        date = match.group('date').strip()
        return location, date
    return None, None  # Return None if no match is found


def parse_html_content(soup: BeautifulSoup) -> pd.DataFrame:
    """
    Parses the HTML content with BeautifulSoup and extracts
    the weather data into a DataFrame.

    Args:
        soup (BeautifulSoup): BeautifulSoup object containing
        the parsed HTML content.

    Returns:
        pd.DataFrame: DataFrame containing the extracted weather data.
    """
    # Extract the page header to get location and date information
    header = soup.find('div', attrs={'class': 'content'}).find('h1')
    location, date = extract_simplified_information(str(header))

    # Find the table containing the weather data
    table = soup.find('table', attrs={'class': 'data'})
    rows = table.find('tbody').find_all('tr')  # Extract all table rows

    # Extract day indexes from table headers
    days = [index.text for row in rows for index in row.find_all('th')]

    # Compile the data for each day from the table rows
    data = [[cell.text if cell.text != '\xa0' else 'NA'
             for cell in row.find_all('td')]
            for row in rows]

    # Convert date string to datetime and format dates for each day
    month_year_datetime = datetime.strptime(date, "%B %Y")
    formatted_dates = [month_year_datetime.replace(day=int(day))
                       .strftime("%Y-%m-%d") for day in days]

    # Define the columns for the DataFrame
    columns = ['Day', 'MinTemp', 'MaxTemp', 'Rainfall',
               'Evaporation', 'Sunshine', 'WindGustDir',
               'WindGustSpeed', 'WindGustTime', 'Temp9am',
               'Humidity9am', 'Cloud9am', 'WindDir9am',
               'WindSpeed9am', 'Pressure9am', 'Temp3pm',
               'Humidity3pm', 'Cloud3pm', 'WindDir3pm',
               'WindSpeed3pm', 'Pressure3pm']
    df = pd.DataFrame(data, columns=columns)

    # Drop unnecessary columns
    df.drop(['Day', 'WindGustTime'], axis=1, inplace=True)

    df['Date'] = formatted_dates
    df['Location'] = location

    return df


def aggregate_weather_data(urls: List[str]) -> pd.DataFrame:
    """
    Aggregates weather data from multiple URLs into a single DataFrame.

    Args:
        urls (List[str]): List of URLs to fetch and parse weather data from.

    Returns:
        pd.DataFrame: Aggregated DataFrame containing weather data
        from all specified URLs.
    """
    aggregated_df = pd.DataFrame()
    for url in urls:
        soup = fetch_page_content(url)
        if soup:
            # Extract weather data into a DataFrame
            df_temp = parse_html_content(soup)
            aggregated_df = pd.concat([aggregated_df, df_temp],
                                      ignore_index=True)
    return aggregated_df
