
class Recommender:

    GENRE_WEIGHT = 3
    ACTOR_WEIGHT = 2
    RATING_WEIGHT = 0.5

    MIN_SIMILARITY = 5

    def __init__(self, catalog):
        self.catalog = catalog

    def _liked_movies(self):
        liked = []
        for movie in self.catalog:
            if movie.user_rating is not None and movie.user_rating >= 7:
                liked.append(movie)
        return liked

    def _build_profile(self, liked):
        fav_genres = set()
        fav_actors = set()
        for movie in liked:
            fav_genres.update(movie.get_genres_list())
            fav_actors.update(movie.get_actors_list())
        return fav_genres, fav_actors

    def _similarity(self, movie, fav_genres, fav_actors):
        score = 0

        for genre in movie.get_genres_list():
            if genre in fav_genres:
                score += self.GENRE_WEIGHT

        for actor in movie.get_actors_list():
            if actor in fav_actors:
                score += self.ACTOR_WEIGHT

        return score

    def recommend(self, count=5):
        liked = self._liked_movies()
        if not liked:
            return []

        fav_genres, fav_actors = self._build_profile(liked)

        scored = []
        for movie in self.catalog:
            if movie.watched:
                continue

            similarity = self._similarity(movie, fav_genres, fav_actors)
            if similarity < self.MIN_SIMILARITY:
                continue

            total = similarity + movie.imdb_rating * self.RATING_WEIGHT
            scored.append((total, movie))

        scored.sort(key=lambda pair: pair[0], reverse=True)

        return [movie for total, movie in scored[:count]]