"""
This module contains functions to transform the Australian meteorology data
"""


from datetime import datetime
from typing import List

import pandas as pd
from bs4 import BeautifulSoup

from Extract.australian_meteorology.australian_meteorology_extract import (
    extract_simplified_information, fetch_page_content)


def parse_html_content(soup: BeautifulSoup) -> pd.DataFrame:
    """
    Parses the HTML content with BeautifulSoup and extracts
    the weather data into a DataFrame.

    :param soup: BeautifulSoup object containing the parsed HTML content.
    :return: DataFrame containing the extracted weather data.
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
    data = [[cell.text if cell.text != '\xa0' else '-1'
             for cell in row.find_all('td')]
            for row in rows]

    for i in range(len(data)):
        for j in range(len(data[i])):
            if data[i][j] == 'Calm':
                data[i].insert(j + 1, -1)

    # Convert date string to datetime and format dates for each day
    month_year_datetime = datetime.strptime(date, "%B %Y")
    formatted_dates = [month_year_datetime.replace(day=int(day))
                       .strftime("%Y-%m-%d") for day in days]

    # Define the columns for the DataFrame
    columns = ['day', 'min_temp', 'max_temp', 'rainfall',
               'evaporation', 'sunshine', 'wind_gust_dir',
               'wind_gust_speed', 'wind_gust_time', 'temp_9am',
               'humidity_9am', 'cloud_9am', 'wind_dir_9am',
               'wind_speed_9am', 'pressure_9am', 'temp_3pm',
               'humidity_3pm', 'cloud_3pm', 'wind_dir_3pm',
               'wind_speed_3pm', 'pressure_3pm']
    df = pd.DataFrame(data, columns=columns)

    # Drop unnecessary columns
    df.drop(['day', 'wind_gust_time'], axis=1, inplace=True)

    df['date'] = formatted_dates
    df['location'] = location

    return df


def aggregate_weather_data(urls: List[str]) -> pd.DataFrame:
    """
    Aggregates weather data from multiple URLs into a single DataFrame.

    :param urls: List of URLs to fetch and parse weather data from.
    :return: Aggregated DataFrame containing weather data from all specified URLs.
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
