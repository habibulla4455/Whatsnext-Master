"""This module will serve the api request."""

from config import client
from app import app
from bson.json_util import dumps
from flask import request, jsonify
import json
import ast
import imp
import numpy as np
import pandas as pd
import pymongo


# Import the helpers module
helper_module = imp.load_source('*', './app/helpers.py')

# Select the database
db = client.whatsnext
# Select the collection
ratings = db.ratings
movies = db.movies

@app.route("/")
def get_initial_response():
    """Welcome message for the API."""
    # Message to the user
    message = {
        'apiVersion': 'v1.0',
        'status': '200',
        'message': 'Welcome to the Flask API'
    }
    # Making the message looks good
    resp = jsonify(message)
    # Returning the object
    return resp


@app.route("/api/v1/movies", methods=['POST'])
def create_user():
    """
       Function to create new users.
       """
    data = request.data
    dataDict = json.loads(data)
    print(dataDict['title'])

    # Recommander 

    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient['whatsnext']

    ratings = mydb['ratings']
    movies = mydb['movies']

    ratings_data = pd.DataFrame(list(ratings.find()))
    movie_names = pd.DataFrame(list(movies.find()))

    movie_data = pd.merge(ratings_data, movie_names, on="movieId")
    movie_data.groupby('title')['rating'].count().sort_values(ascending=False).head()

    ratings_mean_count = pd.DataFrame(movie_data.groupby('title')['rating'].mean())  
    ratings_mean_count['rating_counts'] = pd.DataFrame(movie_data.groupby('title')['rating'].count())  

    user_movie_rating = movie_data.pivot_table(index='userId', columns='title', values='rating')
    user_movie_rating.head()

    # movie rating array
    current_movie_ratings = user_movie_rating[dataDict['title']]

    current_movie_ratings.head()

    movies_like_current_movie = user_movie_rating.corrwith(current_movie_ratings)

    corr_cuurent_movie = pd.DataFrame(movies_like_current_movie, columns=['Correlation'])
    corr_cuurent_movie.dropna(inplace=True)
    corr_cuurent_movie.head()

    corr_cuurent_movie.sort_values('Correlation', ascending=False).head(10)

    corr_cuurent_movie = corr_cuurent_movie.join(ratings_mean_count['rating_counts'])
    corr_cuurent_movie.head()

    return corr_cuurent_movie[corr_cuurent_movie ['rating_counts'] > 50].sort_values('Correlation', ascending=False).head(10).to_json()

    # try:
    #     # Create new users
    #     try:
    #         data = request.data
    #         dataDict = json.loads(data)
    #         # body = ast.literal_eval(json.dumps(request.get_json()))
    #         print(dataDict)
    #     except:
    #         # Bad request as request body is not available
    #         # Add message for debugging purpose
    #         return "", 400

    #     #record_created = collection.insert(body)

    #     # Prepare the response
    #     if isinstance(record_created, list):
    #         # Return list of Id of the newly created item
    #         return jsonify([str(v) for v in record_created]), 201
    #     else:
    #         # Return Id of the newly created item
    #         return jsonify(str(record_created)), 201
    # except:
    #     # Error while trying to create the resource
    #     # Add message for debugging purpose
    #     return "", 500


@app.errorhandler(404)
def page_not_found(e):
    """Send message to the user with notFound 404 status."""
    # Message to the user
    message = {
        "err":
            {
                "msg": "This route is currently not supported."
            }
    }
    # Making the message looks good
    resp = jsonify(message)
    # Sending OK response
    resp.status_code = 404
    # Returning the object
    return resp
