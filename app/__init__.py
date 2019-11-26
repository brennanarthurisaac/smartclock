# -*- coding: utf-8 -*-
"""App constructor

Module description.
"""
from flask import Blueprint
from flask import Flask
from flask_bootstrap import Bootstrap

from config import Config

app = Flask(__name__)
app.config.from_object(Config)
bootstrap = Bootstrap(app)

from app import routes