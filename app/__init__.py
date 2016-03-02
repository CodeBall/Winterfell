#!/usr/bin/env python
# encoding: utf-8
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext import restful
from config import config
import pymongo
import os

app = Flask(__name__)
api = restful.Api(app)

#链接mysql
db = SQLAlchemy(app)

#链接mongodb
client = pymongo.MongoClient('mongodb://localhost:27017')
database = client.mongo_test
collect = database.words

with app.app_context():
    config_name = os.getenv('CONFIG') or 'default'
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    app.config.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS', True)
    db.init_app(app)

from .models import *
from .userManage import *
from .wordManage import *
from .userControl import *
from .wordControl import *
