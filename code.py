# Import necessary libraries
import sqlite3
import pandas as pd
# Create a SQLite database in memory
conn = sqlite3.connect(':memory:')
cursor = conn.cursor()

# Create movies table
cursor.execute('''
    CREATE TABLE movies (
        movie_id INT PRIMARY KEY,
        title TEXT,
        release_year INT,
        genre TEXT
    );
''')

# Create actors table
cursor.execute('''
    CREATE TABLE actors (
        actor_id INT PRIMARY KEY,
        actor_name TEXT
    );
''')

# Create directors table
cursor.execute('''
    CREATE TABLE directors (
        director_id INT PRIMARY KEY,
        director_name TEXT
    );
''')

# Create movie_casts table
cursor.execute('''
    CREATE TABLE movie_casts (
        movie_id INT,
        actor_id INT,
        FOREIGN KEY (movie_id) REFERENCES movies(movie_id),
        FOREIGN KEY (actor_id) REFERENCES actors(actor_id)
    );
''')

# Create movie_directors table
cursor.execute('''
    CREATE TABLE movie_directors (
        movie_id INT,
        director_id INT,
        FOREIGN KEY (movie_id) REFERENCES movies(movie_id),
        FOREIGN KEY (director_id) REFERENCES directors(director_id)
    );
''')

# Commit changes
conn.commit()
# Insert data into the movies table
cursor.executemany('''
    INSERT INTO movies (movie_id, title, release_year, genre) VALUES (?, ?, ?, ?)
''', [
    (1, 'The Matrix', 1999, 'Sci-Fi'),
    (2, 'Inception', 2010, 'Sci-Fi'),
    (3, 'The Dark Knight', 2008, 'Action')
])

# Insert data into the actors table
cursor.executemany('''
    INSERT INTO actors (actor_id, actor_name) VALUES (?, ?)
''', [
    (1, 'Keanu Reeves'),
    (2, 'Leonardo DiCaprio'),
    (3, 'Christian Bale'),
    (4, 'Carrie-Anne Moss'),
    (5, 'Joseph Gordon-Levitt')
])

# Insert data into the directors table
cursor.executemany('''
    INSERT INTO directors (director_id, director_name) VALUES (?, ?)
''', [
    (1, 'Lana Wachowski'),
    (2, 'Christopher Nolan')
])

# Insert data into the movie_casts table (relationship between movies and actors)
cursor.executemany('''
    INSERT INTO movie_casts (movie_id, actor_id) VALUES (?, ?)
''', [
    (1, 1), # Keanu Reeves in The Matrix
    (1, 4), # Carrie-Anne Moss in The Matrix
    (2, 2), # Leonardo DiCaprio in Inception
    (2, 5), # Joseph Gordon-Levitt in Inception
    (3, 3)  # Christian Bale in The Dark Knight
])

# Insert data into the movie_directors table (relationship between movies and directors)
cursor.executemany('''
    INSERT INTO movie_directors (movie_id, director_id) VALUES (?, ?)
''', [
    (1, 1), # Lana Wachowski directed The Matrix
    (2, 2), # Christopher Nolan directed Inception
    (3, 2)  # Christopher Nolan directed The Dark Knight
])

# Commit changes
conn.commit()
# Query all movies
movies_df = pd.read_sql_query('SELECT * FROM movies', conn)
movies_df
# Query Sci-Fi movies
sci_fi_movies_df = pd.read_sql_query("SELECT title FROM movies WHERE genre = 'Sci-Fi'", conn)
sci_fi_movies_df
# Query movies directed by Christopher Nolan
nolan_movies_df = pd.read_sql_query('''
    SELECT m.title
    FROM movies m
    JOIN movie_directors md ON m.movie_id = md.movie_id
    JOIN directors d ON md.director_id = d.director_id
    WHERE d.director_name = 'Christopher Nolan'
''', conn)
nolan_movies_df
# Query actors in 'Inception'
inception_actors_df = pd.read_sql_query('''
    SELECT a.actor_name
    FROM actors a
    JOIN movie_casts mc ON a.actor_id = mc.actor_id
    JOIN movies m ON mc.movie_id = m.movie_id
    WHERE m.title = 'Inception'
''', conn)
inception_actors_df
# Query all movies and their directors
movies_directors_df = pd.read_sql_query('''
    SELECT m.title, d.director_name
    FROM movies m
    JOIN movie_directors md ON m.movie_id = md.movie_id
    JOIN directors d ON md.director_id = d.director_id
''', conn)
movies_directors_df
# Query total number of movies per genre
movies_per_genre_df = pd.read_sql_query('''
    SELECT genre, COUNT(*) as total_movies
    FROM movies
    GROUP BY genre
''', conn)
movies_per_genre_df
# Close the connection to the SQLite database
conn.close()
