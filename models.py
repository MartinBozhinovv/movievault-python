from datetime import datetime


class Movie:

    def __init__(self, imdb_id, title, year, genre='', actors='',
                 plot='', imdb_rating=0.0, poster_url='',
                 user_rating=None, watched=False, date_added=None):

        self.imdb_id = imdb_id
        self.title = title
        self.year = year
        self.genre = genre
        self.actors = actors
        self.plot = plot
        self.imdb_rating = imdb_rating
        self.poster_url = poster_url

        self.user_rating = user_rating
        self.watched = watched

        if date_added is None:
            self.date_added = datetime.now()
        else:
            self.date_added = date_added


    def __str__(self):
        return f"{self.title} ({self.year})"

    def __repr__(self):
        return f"Movie('{self.title}', {self.year})"

    def __eq__(self, other):
        if not isinstance(other, Movie):
            return False
        return self.imdb_id == other.imdb_id

    def __hash__(self):
        return hash(self.imdb_id)

    def __lt__(self, other):
        return self.year < other.year


    def get_genres_list(self):
        if not self.genre:
            return []
        return [g.strip() for g in self.genre.split(',')]

    def get_actors_list(self):
        if not self.actors:
            return []
        return [a.strip() for a in self.actors.split(',')]


class Catalog:

    def __init__(self):
        self.movies = []

    def __len__(self):
        return len(self.movies)

    def __iter__(self):
        return iter(self.movies)

    def __contains__(self, movie):
        return movie in self.movies

    def __str__(self):
        return f"Catalog with {len(self.movies)} movies"


    def add_movie(self, movie):
        if movie in self.movies:
            return False
        self.movies.append(movie)
        return True

    def remove_movie(self, imdb_id):
        for m in self.movies:
            if m.imdb_id == imdb_id:
                self.movies.remove(m)
                return True
        return False

