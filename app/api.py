# -*- coding: utf-8 -*-
"""API

This module contains functions for getting relevant smart information from API.

Weather:
    A function get_weather_html to get a weather report for the configured
    settings in html mode.

News:
    About news.
"""
from json import loads
from requests import get

from typing import List

from config import Config

# Configuration Constants
NEWS_MAX_STORIES = Config.NEWS_MAX_STORIES
NEWS_API_URL = Config.NEWS_API_URL
NEWS_API_PARAMETERS = {
    "country": Config.NEWS_API_COUNTRY,
    "apiKey": Config.NEWS_API_KEY
}
WEATHER_API_URL = Config.WEATHER_API_URL
WEATHER_API_PARAMETERS = {
    "q": Config.WEATHER_API_CITY,
    "mode": "html",
    "appid": Config.WEATHER_API_KEY
}

def get_news_content() -> List:
    """Gets news based on configuration settings and trims the response json
    to the relevant amount of news to give back.
    
    Returns:
        Success: List of articles size NEWS_MAX_STORIES.
        Failure: A string nerror message.
    """
    request = get(NEWS_API_URL, NEWS_API_PARAMETERS)
    if request.status_code == 200:
        content = loads(request.text)
        trimmed_content = content["articles"][:NEWS_MAX_STORIES]
        # This trimms the content to the top amount provided.

        return trimmed_content
    return str(request.status_code) + ": failed to get News."

def get_weather_html() -> str:
    """Gets the weather from a url and with parameters set in configurations.

    Returns:
        Success: The weather html string.
        Failure: A string error message.
    """
    request = get(WEATHER_API_URL, WEATHER_API_PARAMETERS)
    if request.status_code == 200:
        return request.text
    return str(request.status_code) + ": failed to get Weather."
