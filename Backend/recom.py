import numpy as np
import pandas as pd
import pymongo

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

#movie rating array
current_movie_ratings = user_movie_rating['Caddyshack (1980)']

current_movie_ratings.head()

movies_like_current_movie = user_movie_rating.corrwith(current_movie_ratings)

corr_cuurent_movie = pd.DataFrame(movies_like_current_movie, columns=['Correlation'])
corr_cuurent_movie.dropna(inplace=True)
corr_cuurent_movie.head()

corr_cuurent_movie.sort_values('Correlation', ascending=False).head(10)

corr_cuurent_movie = corr_cuurent_movie.join(ratings_mean_count['rating_counts'])
corr_cuurent_movie.head()

print(corr_cuurent_movie[corr_cuurent_movie ['rating_counts'] > 50].sort_values('Correlation', ascending=False).head(20))