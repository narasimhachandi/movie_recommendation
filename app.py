import streamlit as st
import pickle
import requests
import pandas as pd

st.title('MOVIE RECOMMENDATION ENGINE')

movies = pd.read_pickle('movies.pkl')
list_of_movies = movies['title'].values
similarity = pd.read_pickle('similarity.pkl')

selected_movie = st.selectbox(
    'Select the movie you liked from the dropdown',
    list_of_movies)

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US'.format(movie_id))
    data = response.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    similar = similarity[movie_index]
    movie_list = sorted(list(enumerate(similar)),reverse=True, key = lambda x:x[1])[1:6]
    
    recommended_movies = []
    recommended_movies_poster = []
    for i in movie_list:
        movie_id = movies.iloc[i[0]].id

        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_poster.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_poster

if st.button('Recommend Movies'):
    st.write('You may also like :')
    names, posters = recommend(selected_movie)
    
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])
                                            
