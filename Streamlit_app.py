import streamlit as st
import pickle
import requests

# Load data
with open("movies.pkl", "rb") as f:
    movies = pickle.load(f)

with open("similarity.pkl", "rb") as f:
    similarity = pickle.load(f)

# Your OMDb API Key
OMDB_API_KEY = "c42495a7"  # Replace with your actual OMDb key

# Function to fetch poster
def fetch_poster(title):
    url = f"http://www.omdbapi.com/?t={title}&apikey={OMDB_API_KEY}"
    resp = requests.get(url)
    try:
        data = resp.json()
        return data.get("Poster", "")
    except:
        return ""

# Recommend function
def recommend(movie):
    movie = movie.lower()
    movie_index = None

    for idx, m in enumerate(movies):
        if m["title"].lower() == movie:
            movie_index = idx
            break

    if movie_index is None:
        return []

    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = [movies[i[0]]["title"] for i in movie_list]
    return recommended_movies

# Streamlit UI
st.title("🎬 Movie Recommendation System")

selected_movie = st.text_input("Enter a movie title")

if selected_movie:
    results = recommend(selected_movie)
    if results:
        st.subheader("Recommended Movies:")

        cols = st.columns(len(results))
        for i, r in enumerate(results):
            with cols[i]:
                st.image(fetch_poster(r), width=150)
                st.markdown(f"**{r}**")
    else:
        st.error("Movie not found. Please try another title.")
