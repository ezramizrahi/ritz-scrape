Scraper for my local movie theatre. Scrapes movies, showtimes, and then grabs genres (from TMDB).

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

## Tests
Tests are located in the `tests` directory and run as part of the build process.