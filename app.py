import streamlit as st
import pickle
import pandas as pd
import requests

import os

import gdown

def download_file(file_id, output):
    if not os.path.exists(output):
        url = f"https://drive.google.com/uc?id={file_id}"
        gdown.download(url, output, quiet=False)


def fetch_poster(movie_id):
    url = ("https://api.themoviedb.org/3/movie/{"
           "}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US").format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]

    movies_list = sorted(enumerate(distances), key=lambda x: x[1], reverse=True)

    recommended_movies = []
    recommended_movie_posters = []
    for i in movies_list[1:6]:  # skip itself, take top 5
        movie_id = movies.iloc[i[0]].movie_id

        recommended_movies.append(movies.iloc[i[0]].title)
        # fetch poster from API
        recommended_movie_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_movie_posters

movies_dict = pickle.load(open('movie_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)

file_id = "1Sa7gOJ2ZGxUluefIu3NM-5ealQrLv3n3"  # just the ID
download_file(file_id, "similarity.pkl")
similarity = pickle.load(open('similarity.pkl','rb'))

st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
'Browse Movies',
movies['title'].values  )

if st.button('Recommend'):
    names,posters = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.caption(names[0])
        st.image(posters[0])
    with col2:
        st.caption(names[1])
        st.image(posters[1])
    with col3:
        st.caption(names[2])
        st.image(posters[2])
    with col4:
        st.caption(names[3])
        st.image(posters[3])
    with col5:
        st.caption(names[4])
        st.image(posters[4])