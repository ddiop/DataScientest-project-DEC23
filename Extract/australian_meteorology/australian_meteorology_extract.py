"""
This module contains functions to extract weather data from the
    Australian Bureau of Meteorology website.
"""


from itertools import product
import re
from typing import List, Optional, Tuple

from bs4 import BeautifulSoup
import requests


def generate_urls(dates: List[str], locations: List[str]) -> List[str]:
    """
    Generates URLs for weather data based on specified dates and locations.

    Documentation:
        Further details on the website can be found at:
            https://reg.bom.gov.au

    :arg dates: List of dates for which to fetch weather data.
    :arg locations: List of location codes to fetch weather data for.
    :returns: List of URLs constructed based on the specified dates and locations.
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

    :arg url: The URL from which to fetch the content.
    :returns: BeautifulSoup object containing the parsed HTML content,
        or None if the request fails.
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


def extract_simplified_information(html: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Extracts simplified location and date information from the HTML
    content of a page.

    :arg html: HTML content as a string.
    :returns: A tuple containing the location and date, or None if not found.
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
    return None, None  # Return a tuple of None if no match is found
