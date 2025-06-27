import streamlit as st
import pickle
import requests
from sklearn.metrics.pairwise import cosine_similarity

# Load movie data
movies = pickle.load(open("movies.pkl", "rb"))
similarity = pickle.load(open("similarity.pkl", "rb"))

# Get OMDb API key from Streamlit secrets
OMDB_API_KEY = st.secrets["c42495a7"]

def fetch_poster(title):
    url = f"http://www.omdbapi.com/?t={title}&apikey={OMDB_API_KEY}"
    response = requests.get(url)
    data = response.json()
    if data.get("Response") == "True":
        return data.get("Poster")
    else:
        return "https://via.placeholder.com/150?text=No+Image"

def recommend(movie_title):
    movie_index = None
    for idx, title in enumerate(movies['title']):
        if title.lower() == movie_title.lower():
            movie_index = idx
            break
    if movie_index is None:
        return []

    distances = list(enumerate(similarity[movie_index]))
    recommended = sorted(distances, key=lambda x: x[1], reverse=True)[1:6]
    recommended_movies = [movies['title'][i] for i, _ in recommended]
    return recommended_movies

# Streamlit UI
st.set_page_config(page_title="Movie Recommender", layout="wide")
st.title("🎬 Movie Recommendation System")

selected_movie = st.selectbox("Enter a movie title", movies['title'].values)

if st.button("Recommend"):
    recommendations = recommend(selected_movie)
    if recommendations:
        cols = st.columns(len(recommendations))
        for i, movie in enumerate(recommendations):
            with cols[i]:
                st.text(movie)
                st.image(fetch_poster(movie), width=150)
    else:
        st.error("Sorry, no recommendations found.")
