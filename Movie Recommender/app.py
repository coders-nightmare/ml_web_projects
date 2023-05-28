import streamlit as st
import pickle
import pandas as pd

import requests


def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?language=en-US".format(
        movie_id)

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI4MGZkYjVjOGJmOWE1Njk1YWIxNDEyMzJhYWIxNmUzMyIsInN1YiI6IjY0NmY4MjA5NzcwNzAwMDBmYzAxZWMxMyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.RzECbXS8xf4umru2leTuK4VO7bg8oTsTm12ZtUKNKMY"
    }

    response = requests.get(url, headers=headers)
    data = response.json()
    # print(data)
    # print("-----------------------------------------------------")
    return "https://image.tmdb.org/t/p/w500/"+data['poster_path']


# loading our model movies dictionary
movies_dict = pickle.load(
    open('E:\DataSets\pickle_files\movies_dict.pkl', 'rb'))

movies = pd.DataFrame(movies_dict)

# loading similarity array
similarity = pickle.load(
    open('E:\DataSets\pickle_files\similarity.pkl', 'rb'))


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    top_movies_index = sorted(
        list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = []
    recommended_movies_posters = []
    for i in top_movies_index:
        movie_id = movies.iloc[i[0]].movie_id
        # fetching poster from api
        recommended_movies_posters.append(fetch_poster(movie_id))
        recommended_movies.append(movies.iloc[i[0]].title)
    return recommended_movies, recommended_movies_posters


#
# to display text
st.title("Movie Recommender System")


selected_movie_name = st.selectbox(
    'How would you like to be contacted?',
    movies['title'].values)

st.write('You selected:', selected_movie_name)

if st.button('Recommend'):
    recommended_movies, recommended_moveis_poster = recommend(
        selected_movie_name)
    # for i in range(len(recommended_movies)):
    #     st.write(recommended_movies[i])
    #     st.write(recommended_moveis_poster[i])
    col1, col2, col3 = st.columns(3)

    with col1:
        st.header(recommended_movies[0])
        st.image(recommended_moveis_poster[0])
    with col2:
        st.header(recommended_movies[1])
        st.image(recommended_moveis_poster[1])
    with col3:
        st.header(recommended_movies[2])
        st.image(recommended_moveis_poster[2])
    col4, col5 = st.columns(2)
    with col4:
        st.header(recommended_movies[3])
        st.image(recommended_moveis_poster[3])
    with col5:
        st.header(recommended_movies[4])
        st.image(recommended_moveis_poster[4])
