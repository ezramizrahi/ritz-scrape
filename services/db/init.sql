CREATE TABLE movies (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    added_at TIMESTAMP DEFAULT current_timestamp
);

CREATE TABLE showtimes (
    id SERIAL PRIMARY KEY,
    movie_id INT REFERENCES movies(id),
    time VARCHAR(255)
);

CREATE TABLE genres (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE
);

CREATE TABLE movie_genres (
    movie_id INT REFERENCES movies(id),
    genre_id INT REFERENCES genres(id),
    PRIMARY KEY (movie_id, genre_id)
);