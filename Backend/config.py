"""This module is to configure app to connect with database."""

from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
DEBUG = True
DATABASE = MongoClient()['whatsnext'] # DB_NAME
