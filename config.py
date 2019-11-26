# -*- coding: utf-8 -*-
"""Config object

This module stores a configurations class consisting of attributes (settings)
used both by flask and other parts of the program.

Some values are pulled from a config.json file.
"""
import os

from json import load

with open("config.json", "r") as config_file:
    CONFIG_DATA = load(config_file)

class Config:
    """Properties/attributes class for the Flask application.

    Attributes:
        SECRET_KEY (str): Encryption key used for passing secure form
            information.
        
        TTS_MESSAGE (str): A format string broadcasted in text-to-speach when
            an alarm is raised.

        WEATHER_API_URL (str): Api url for getting weather.
        WEATHER_API_CITY (str): City to report weather on.
        WEATHER_API_KEY (str): Unique app key used in get requests.

        NEWS_MAX_STORIES (int): Amount of news entries to display.
        NEWS_API_URL (str): Api url for getting news.
        NEWS_API_COUNTRY (str): A short code used to identify the country for
            relevant news.
        NEWS_API_KEY (str): Unique app key used in get requests.
    """
    SECRET_KEY = (os.environ.get("SECRET_KEY")
                  or CONFIG_DATA["backup_secret_key"])
    TTS_MESSAGE = CONFIG_DATA["tts_message"]
    WEATHER_API_URL = CONFIG_DATA["weather_api"]["url"]
    WEATHER_API_CITY = CONFIG_DATA["weather_api"]["city"]
    WEATHER_API_KEY = CONFIG_DATA["weather_api"]["api_key"]
    NEWS_MAX_STORIES = CONFIG_DATA["news_api"]["max_stories"]
    NEWS_API_URL = CONFIG_DATA["news_api"]["url"]
    NEWS_API_COUNTRY = CONFIG_DATA["news_api"]["country"]
    NEWS_API_KEY = CONFIG_DATA["news_api"]["api_key"]
