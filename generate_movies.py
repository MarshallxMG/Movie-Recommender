import requests
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Replace with your OMDb API Key
API_KEY = "c42495a7"

# List of known movie titles (you can add more)
movie_titles = [
    "The Matrix", "Inception", "Avatar", "Titanic", "Interstellar", 
    "The Dark Knight", "Gladiator", "Forrest Gump", "The Avengers", "Joker"
]

# Fetch movie data from OMDb
movies = []
for title in movie_titles:
    url = f"http://www.omdbapi.com/?apikey={API_KEY}&t={title}"
    res = requests.get(url)
    data = res.json()

    if data.get("Response") == "True":
        movie_info = {
            'title': data.get('Title', ''),
            'tags': f"{data.get('Genre', '')} {data.get('Director', '')} {data.get('Actors', '')} {data.get('Plot', '')}"
        }
        movies.append(movie_info)
        print(f"Fetched: {title}")
    else:
        print(f"Failed to fetch: {title} - {data.get('Error')}")

# Ensure we got data
if not movies:
    print("No movie data fetched. Check API key or titles.")
    exit()

# Extract tags and vectorize
movie_tags = [movie['tags'] for movie in movies]
vectorizer = CountVectorizer(stop_words='english')
vectors = vectorizer.fit_transform(movie_tags)

# Compute cosine similarity
similarity = cosine_similarity(vectors)

# Save files
with open('movies.pkl', 'wb') as f:
    pickle.dump(movies, f)

with open('similarity.pkl', 'wb') as f:
    pickle.dump(similarity, f)

print("✅ Data saved as movies.pkl and similarity.pkl")
