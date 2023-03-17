import pandas as pd
import numpy as np
from flask import Flask
from flask import Flask, request, render_template, Response, jsonify
from flask_ngrok import run_with_ngrok
import json

app = Flask(__name__)

movies_df = pd.read_csv("./100k/movies.csv")
ratings_df = pd.read_csv("./100k/ratings.csv")
merged_df_on_movieId = pd.merge(ratings_df, movies_df, on='movieId')
merged_df_on_movieId = merged_df_on_movieId.drop(['timestamp', 'genres'], axis=1)
movie_ratingCount = (merged_df_on_movieId.groupby(by = ['title'])['rating'].count().reset_index().
                     rename(columns = {'rating': 'totalRatingCount'})[['title', 'totalRatingCount']])
rating_with_totalRatingCount = merged_df_on_movieId.merge(movie_ratingCount, left_on = 'title', right_on = 'title', how = 'left')
user_rating = rating_with_totalRatingCount.drop_duplicates(['userId','title'])

# Item Based Filtering
movie_user_rating_pivot = user_rating.pivot(index = 'userId', columns = 'title', values = 'rating').fillna(0)

X = movie_user_rating_pivot.values.T #extracted the values

Y = movie_user_rating_pivot.values

import sklearn
from sklearn.decomposition import TruncatedSVD #Imported truncated singular value Decomposition which reduces the dimention of the matrix

SVD = TruncatedSVD(n_components=12, random_state=17) # intantiated SVD with the number of columns finally
matrix = SVD.fit_transform(X) # fit and transform

import warnings
warnings.filterwarnings("ignore",category =RuntimeWarning)
movies_corr = np.corrcoef(matrix)  # Getting the correlation coefficients

movie_title = movie_user_rating_pivot.columns # To get all the movies
movie_title_list = list(movie_title)
#coffey_hands = movie_title_list.index("Guardians of the Galaxy (2014)") # extracting the index of the movie we wanted to get the recommendations for

#corr_coffey_hands  = movies_corr[coffey_hands] # Extracting the correlation coefficients of other movies based on the movie we are searching
#print(list(movie_title[(corr_coffey_hands >= 0.95)]))

# _____________________________________ USer Recommendation

SVD = TruncatedSVD(n_components=12, random_state=17) # intantiated SVD with the number of columns finally
user_matrix = SVD.fit_transform(Y) # fit and transform 
user_matrix.shape

import warnings
warnings.filterwarnings("ignore",category =RuntimeWarning)
user_corr = np.corrcoef(user_matrix)  # Getting the correlation coefficients
user_corr.shape

user_ids = movie_user_rating_pivot.T.columns
user_id_list = list(user_ids)
user_index = user_id_list.index(10) # You can enter the user id of your choice

user_specific_corr  = user_corr[user_index] # Extracting the correlation coefficients of other movies based on the movie we are searching
list(user_ids[(user_specific_corr >= 0.9)])


@app.route('/recommend-movie' , methods=[ "GET" , "POST" ])
def index():
    q = request.args.get("q") 

    coffey_hands = movie_title_list.index(q) # extracting the index of the movie we wanted to get the recommendations for
    corr_coffey_hands  = movies_corr[coffey_hands] # Extracting the correlation coefficients of other movies based on the movie we are searching
    
    return list(movie_title[(corr_coffey_hands >= 0.95)])

if __name__ == "__main__" :
    app.run(debug=True)