import json
from bs4 import BeautifulSoup
import requests
from db_logic.db_actions import insert_movie, insert_showtime, insert_genre, associate_movie_genre
from utils import get_movie_details, find_best_match, get_movie_genres_by_id
from dotenv import load_dotenv
load_dotenv()

print("Starting scraper...")

url = "https://www.ritzcinemas.com.au/now-showing"
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

print("Scraping movie titles and times...")

movies_dict = {}
for li in soup.select('ul.Sessions > li[data-name]'):
    title = li['data-name']
    times = [span.text for span in li.select('a > span.Time')]
    
    if title in movies_dict:
        movies_dict[title].extend(times)
    else:
        movies_dict[title] = times

print(f"Found {len(movies_dict)} unique movie titles.")

for title, times in movies_dict.items():
    print(f"Processing movie: {title}")
    details = get_movie_details(title)
    candidates = details.get('results', [])
    candidate_map = {result['title']: result for result in candidates}
    candidate_titles = list(candidate_map.keys())
    
    movie_id_db = None
    
    if candidate_titles:
        best_match_title = find_best_match(title, candidate_titles)
        best_match_object = candidate_map.get(best_match_title)
        print(f"Best match for {title} is {best_match_title}.")

        if best_match_object:
            movie_id = best_match_object.get('id')
            genres, title = get_movie_genres_by_id(movie_id)
            
            if genres:
                print(f"Inserting movie and genres into database: {title}, {genres}")
                movie_id_db = insert_movie(title)
                for genre in genres:
                    genre_id = insert_genre(genre)
                    if genre_id:
                        associate_movie_genre(movie_id_db, genre_id)
    else:
        print(f"No matching candidates found for {title}.")
        
    # If no best match or genres, insert only the movie and showtimes
    if not movie_id_db:
        print(f"Inserting only movie and showtimes into database: {title}")
        movie_id_db = insert_movie(title)
        
    for time in times:
        insert_showtime(movie_id_db, time)

print("Scraper finished successfully.")
