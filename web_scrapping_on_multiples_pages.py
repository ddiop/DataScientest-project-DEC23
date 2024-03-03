"""
This script is designed to scrape weather data from the
Australian Bureau of Meteorology website.
It automates the process of gathering weather observations from
multiple locations and dates, consolidating the data into a single,
structured format for analysis.

Usage:
To use this script, define the dates and location codes you wish to scrape
in the `dates_to_scrape` and `locations_to_scrape` variables. The script will
then automatically generate the necessary URLs, scrape the weather data,
and print the consolidated DataFrame.

Note:
This script is tailored to the specific structure of the weather
data pages on the Australian Bureau of Meteorology website.
Changes to the website's layout or data presentation may
require adjustments to the script's parsing logic.
"""


from datetime import datetime
from itertools import product
from typing import List, Tuple, Optional

import re
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests


def generate_urls(dates: List[str], locations: List[str]) -> List[str]:
    """Generates a list of URLs based on given dates and locations."""
    base_url = ("https://reg.bom.gov.au/climate/dwo/{date}/"
                "html/IDCJDW{location}.{date}.shtml")
    return [base_url.format(date=date, location=location)
            for date, location in product(dates, locations)]


def fetch_page_content(url: str) -> Optional[bs]:
    """Fetches HTML content from a given URL."""
    try:
        response = requests.get(url, timeout=1000)
        response.raise_for_status()
        return bs(response.content, 'lxml')
    except requests.RequestException as e:
        print(f"Error fetching URL {url}: {e}")
        return None


def extract_simplified_information(html: str)\
        -> Tuple[Optional[str], Optional[str]]:
    """Extracts simplified location and date information from HTML code."""
    match = re.search(r"<h1>(?P<location>.+?)(?:<br/?>|,)"
                      r"\s*(?P<date>\w+ \d{4})", html, re.IGNORECASE)
    if match:
        location = match.group('location').split(',')[0].strip()
        date = match.group('date').strip()
        return location, date
    return None, None


def parse_html_content(soup: bs) -> pd.DataFrame:
    """
    Parses HTML content and extracts weather data into a DataFrame.

    Args:
        soup (bs): BeautifulSoup object containing the parsed HTML content.

    Returns:
        df (pd.DataFrame): DataFrame containing the extracted weather data.
    """
    # Extracting location and date from the page header
    header = soup.find('div', attrs={'class': 'content'}).find('h1')
    location, date = extract_simplified_information(str(header))

    # Find the table in the HTML that contains the weather data
    table = soup.find('table', attrs={'class': 'data'})

    # Extract all rows from the table body
    rows = table.find('tbody').find_all('tr')

    # Extracting table indexes (days of the month)
    days = [index.text for i in range(len(rows))
            for index in rows[i].find_all('th')]

    # Extracting weather data for each day
    data = []
    for row in rows:
        day_data = [data.text if data.text != '\xa0' else 'NA'
                    for data in row.find_all('td')]
        data.append(day_data)

    # Formatting the date information
    month_year_datetime = datetime.strptime(str(date), "%B %Y")
    formatted_dates = [month_year_datetime.replace(day=int(day))
                       .strftime("%Y-%m-%d") for day in days]

    # Define column names for the DataFrame
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

    # Add formatted date and location to the DataFrame
    df['Date'] = formatted_dates
    df['Location'] = location

    return df


def aggregate_weather_data(urls: List[str]) -> pd.DataFrame:
    """Aggregates weather data from multiple URLs into a single DataFrame."""
    aggregated_df = pd.DataFrame()
    for url in urls:
        soup = fetch_page_content(url)
        if soup:
            df_temp = parse_html_content(soup)
            aggregated_df = pd.concat([aggregated_df, df_temp],
                                      ignore_index=True)
    return aggregated_df

