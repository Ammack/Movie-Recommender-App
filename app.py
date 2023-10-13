import streamlit as st

st.set_page_config(
    page_title="Movie Recommendation App",
    page_icon="🧊",
    layout="wide",
)

st.title("Movie Recommender")


import pickle
import pandas as pd
import numpy as np
import requests

movies_list = pd.read_pickle(open("movies.pkl", "rb"))

similarity = pd.read_pickle(open("similarity.pkl", "rb"))

def poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path


def recommend(movie):
    movie_index = movies_list[movies_list["title"] == movie].index[0]
    top_similarities = sorted(list(enumerate(similarity[movie_index])), reverse=True, key=lambda x: x[1])[1:21]
    recommendation = []
    posters = []
    for i in top_similarities:

        movie_id = movies_list.iloc[i[0]].movie_id
        recommendation.append(movies_list.iloc[i[0]].title)

        # fetching posters from API
        posters.append(poster(movie_id))

    return recommendation, posters


option = st.selectbox(
    "Select Movie to get Recommendation", (movies_list["title"].values)
)


if st.button("Recommend"):
    recommendation, posters = recommend(option)

    col = st.columns(5,gap="large")
    col2 = st.columns(5,gap="large")
    col3 = st.columns(5,gap="large")
    for i in range(5):    

        with col[i]:
            st.image(posters[i])
            st.text(recommendation[i])

        with col2[i]:
            st.image(posters[i+5])
            st.text(recommendation[i+5])

        with col3[i]:
            st.image(posters[i+10])
            st.text(recommendation[i+10])