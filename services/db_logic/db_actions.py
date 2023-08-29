import psycopg2
import os

connection_pool = psycopg2.pool.SimpleConnectionPool(
    minconn=1,
    maxconn=10,
    host=os.getenv("DB_HOST"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
)

def get_conn():
    return connection_pool.getconn()

def release_conn(conn):
    connection_pool.putconn(conn)

def insert_movie(title):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO movies (title) VALUES (%s) RETURNING id;", (title,))
    movie_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    release_conn(conn)
    return movie_id

def insert_showtime(movie_id, time):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO showtimes (movie_id, time) VALUES (%s, %s);", (movie_id, time))
    conn.commit()
    cur.close()
    release_conn(conn)

def insert_genre(genre):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO genres (name) VALUES (%s) ON CONFLICT (name) DO NOTHING RETURNING id;", (genre,))
    genre_id = cur.fetchone()
    if genre_id is None:
        cur.execute("SELECT id FROM genres WHERE name = %s;", (genre,))
        genre_id = cur.fetchone()
    if genre_id is not None:
        genre_id = genre_id[0]
    conn.commit()
    cur.close()
    release_conn(conn)
    return genre_id

def associate_movie_genre(movie_id, genre_id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO movie_genres (movie_id, genre_id) VALUES (%s, %s) ON CONFLICT DO NOTHING;", (movie_id, genre_id))
    conn.commit()
    cur.close()
    release_conn(conn)
