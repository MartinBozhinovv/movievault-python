import urllib.request
import urllib.parse
import urllib.error
import json
from models import Movie


class OMDbAPI:

    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = 'http://www.omdbapi.com/'

    def search_by_title(self, title):
        params = {
            't': title,
            'apikey': self.api_key
        }
        return self._make_request(params)

    def _make_request(self, params):
        query_string = urllib.parse.urlencode(params)
        url = self.base_url + '?' + query_string

        try:
            with urllib.request.urlopen(url) as response:
                raw_data = response.read()
                data = json.loads(raw_data)
        except urllib.error.URLError:
            return None

        if data.get('Response') == 'False':
            return None

        return self._json_to_movie(data)

    def _json_to_movie(self, data):
        return Movie(
            imdb_id=data.get('imdbID', ''),
            title=data.get('Title', ''),
            year=self._parse_year(data.get('Year', '')),
            genre=data.get('Genre', ''),
            actors=data.get('Actors', ''),
            plot=data.get('Plot', ''),
            imdb_rating=self._parse_rating(data.get('imdbRating', '')),
            poster_url=data.get('Poster', '')
        )

    def _parse_year(self, year_str):
        try:
            return int(year_str[:4])
        except (ValueError, TypeError):
            return 0

    def _parse_rating(self, rating_str):
        try:
            return float(rating_str)
        except (ValueError, TypeError):
            return 0.0