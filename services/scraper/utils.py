import os
import requests
from urllib.parse import quote
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def get_movie_details(movie_title):
    tmdb_url = os.getenv("TMDB_URL")
    api_key = os.getenv("API_KEY")
    if movie_title.startswith("35mm") or movie_title.startswith("70mm"):
        movie_title = movie_title[5:]
    uri_encoded_title = quote(movie_title)
    search_url = f"{tmdb_url}/3/search/movie?api_key={api_key}&query={uri_encoded_title}&include_adult=false&language=en-US&page=1"
    try:
        response = requests.get(search_url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        print(f"Response status code: {response.status_code}")
        return None

def get_movie_genres_by_id(movie_id):
    tmdb_url = os.getenv("TMDB_URL")
    api_key = os.getenv("API_KEY")
    search_url = f"{tmdb_url}/3/movie/{movie_id}?api_key={api_key}&language=en-US"
    try:
        response = requests.get(search_url)
        response.raise_for_status()
        data = response.json()
        genres = [genre['name'] for genre in data.get("genres", [])]
        title = data.get("title", "Unknown")
        print(f"Genres for {title}: {genres}")
        return genres, title
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        print(f"Response status code: {response.status_code}")
        return None

def find_best_match(title, candidates):
    vectorizer = CountVectorizer().fit_transform([title] + candidates)
    vectors = vectorizer.toarray()
    cosine_matrix = cosine_similarity(vectors)
    similarity_scores = list(enumerate(cosine_matrix[0]))
    index = sorted(similarity_scores, key=lambda x: x[1], reverse=True)[1][0] - 1
    return candidates[index]
