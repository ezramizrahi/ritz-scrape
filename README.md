Scraper for my local movie theatre. Scrapes movies, showtimes, and then grabs genres (from TMDB). A lot of this is overkill - it doesn't really need to be run in Docker. We definitely don't need Prometheus. Both of these are included for learning purposes.

## How it works
Scrapes movie titles and showtimes from the "now showing" section of my local movie theatre.

I then search for the movie using using TMDB's api (https://api.themoviedb.org/3/search/movie) - this returns an array of objects with titles similar to our query title. 

I find the closest match using scikit and cosine similarity - this is probably overkill as we will never be comparing the search query against a large amount of potential matches, so I may use Levenshtein distance in the future as it's more than adequate for smaller searches. 

Once we have a match, I grab genre details for the movie.

Currently running this on a Raspberry Pi Model 4 B.

## Requirements
You will need a `.env` file with:
- TMDB api key
- Postgres DB env variables

## Run
1. `docker-compose build --no-cache`
2. `docker-compose up -d`

## Check logs that everything is running properly:
1. `docker-compose logs scraper`
2. `docker-compose logs db`

## Observability
Playing around with observability. I expose some metrics in `observability/expose_metrics.py`. Once you've got it up and running, you can navigate to `http://<raspberry-pi-ip>:9090` and use the Prometheus dashboard.

## Tests
Tests are located in the `tests` directory and run as part of the build process.

## To Do
Remove Docker and Prometheus - too much bloat and not really necessary.