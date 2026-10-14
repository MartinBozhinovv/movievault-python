
import sqlite3
from datetime import datetime
from models import Movie


class Database:

    def __init__(self, db_name='movievault.db'):
        self.conn = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS movies (
                imdb_id TEXT PRIMARY KEY,
                title TEXT,
                year INTEGER,
                genre TEXT,
                actors TEXT,
                plot TEXT,
                imdb_rating REAL,
                poster_url TEXT,
                user_rating INTEGER,
                watched INTEGER,
                date_added TEXT
            )
        ''')
        self.conn.commit()

    def add_movie(self, movie):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO movies
            (imdb_id, title, year, genre, actors, plot,
             imdb_rating, poster_url, user_rating, watched, date_added)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            movie.imdb_id,
            movie.title,
            movie.year,
            movie.genre,
            movie.actors,
            movie.plot,
            movie.imdb_rating,
            movie.poster_url,
            movie.user_rating,
            1 if movie.watched else 0,
            movie.date_added.isoformat()
        ))
        self.conn.commit()

    def get_all_movies(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM movies')
        rows = cursor.fetchall()

        movies = []
        for row in rows:
            movie = self._row_to_movie(row)
            movies.append(movie)
        return movies

    def delete_movie(self, imdb_id):
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM movies WHERE imdb_id = ?', (imdb_id,))
        self.conn.commit()

    def _row_to_movie(self, row):
        return Movie(
            imdb_id=row[0],
            title=row[1],
            year=row[2],
            genre=row[3],
            actors=row[4],
            plot=row[5],
            imdb_rating=row[6],
            poster_url=row[7],
            user_rating=row[8],
            watched=bool(row[9]),
            date_added=datetime.fromisoformat(row[10]) if row[10] else None
        )

    def close(self):
        self.conn.close()