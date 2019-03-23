"""This is init module."""

from flask import Flask
from flask_cors import CORS, cross_origin


# Place where app is defined
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'



from app import usersData
