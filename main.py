import io
import os
import urllib.request
import urllib.error
import ssl
import certifi

import wx
from PIL import Image

from models import Catalog
from database import Database
from omdb_api import OMDbAPI
from recommender import Recommender
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OMDB_API_KEY")

POSTER_WIDTH = 200
POSTER_HEIGHT = 300


class MovieVaultFrame(wx.Frame):

    def __init__(self):
        super().__init__(None, title='MovieVault', size=(920, 620))

        # Данни и модули
        self.db = Database()
        self.api = OMDbAPI(API_KEY)
        self.catalog = Catalog()
        self.found_movie = None
        self.displayed = []

        self.InitUI()
        self.load_from_db()
        self.Centre()
        self.Show()

    def InitUI(self):
        panel = wx.Panel(self)

        wx.StaticText(panel, label='Заглавие:', pos=(20, 22))
        self.search_input = wx.TextCtrl(panel, pos=(90, 18), size=(300, 26))
        search_btn = wx.Button(panel, label='Търси', pos=(400, 16))
        search_btn.Bind(wx.EVT_BUTTON, self.OnSearch)
        add_btn = wx.Button(panel, label='Добави', pos=(500, 16))
        add_btn.Bind(wx.EVT_BUTTON, self.OnAdd)

        self.result_label = wx.StaticText(panel, label='', pos=(20, 55), size=(880, 22))

        self.list_ctrl = wx.ListCtrl(panel, pos=(20, 85), size=(620, 300),style=wx.LC_REPORT)
        self.list_ctrl.InsertColumn(0, 'Заглавие', width=170)
        self.list_ctrl.InsertColumn(1, 'Жанр', width=180)
        self.list_ctrl.InsertColumn(2, 'Година', width=70)
        self.list_ctrl.InsertColumn(3, 'IMDb', width=70)
        self.list_ctrl.InsertColumn(4, 'Моя оценка', width=80)
        self.list_ctrl.InsertColumn(5, 'Гледан', width=70)
        self.list_ctrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnSelectMovie)

        blank = wx.Bitmap(POSTER_WIDTH, POSTER_HEIGHT)
        self.poster = wx.StaticBitmap(panel, bitmap=blank,
                                      pos=(660, 85), size=(POSTER_WIDTH, POSTER_HEIGHT))

        del_btn = wx.Button(panel, label='Изтрий', pos=(20, 400))
        del_btn.Bind(wx.EVT_BUTTON, self.OnDelete)

        watched_btn = wx.Button(panel, label='Маркирай гледан', pos=(100, 400))
        watched_btn.Bind(wx.EVT_BUTTON, self.OnToggleWatched)

        wx.StaticText(panel, label='Оценка:', pos=(255, 405))
        self.rating_input = wx.TextCtrl(panel, pos=(310, 400), size=(45, 26))
        rate_btn = wx.Button(panel, label='Оцени', pos=(365, 400))
        rate_btn.Bind(wx.EVT_BUTTON, self.OnRate)

        rec_btn = wx.Button(panel, label='Препоръки', pos=(455, 400))
        rec_btn.Bind(wx.EVT_BUTTON, self.OnRecommend)

        close_btn = wx.Button(panel, label='Изход', pos=(560, 400))
        close_btn.Bind(wx.EVT_BUTTON, self.OnClose)

        self.rec_label = wx.StaticText(panel, label='', pos=(20, 445), size=(620, 120))


    def load_from_db(self):
        for movie in self.db.get_all_movies():
            self.catalog.add_movie(movie)
        self.refresh_list()

    def refresh_list(self):
        self.list_ctrl.DeleteAllItems()
        self.displayed = list(self.catalog)
        for i, movie in enumerate(self.displayed):
            self.list_ctrl.InsertItem(i, movie.title)
            self.list_ctrl.SetItem(i, 1, movie.genre)
            self.list_ctrl.SetItem(i, 2, str(movie.year))
            self.list_ctrl.SetItem(i, 3, str(movie.imdb_rating))
            rating = str(movie.user_rating) if movie.user_rating is not None else '-'
            self.list_ctrl.SetItem(i, 4, rating)
            self.list_ctrl.SetItem(i, 5, 'Да' if movie.watched else 'Не')

    def get_selected_movie(self):
        index = self.list_ctrl.GetFirstSelected()
        if index == -1:
            self.result_label.SetLabel('Първо избери филм от списъка.')
            return None
        return self.displayed[index]

    def _load_poster(self, url):
        if not url or url == 'N/A':
            return None

        try:
            ssl_context = ssl.create_default_context(cafile=certifi.where())

            with urllib.request.urlopen(url, context=ssl_context) as response:
                raw_data = response.read()
        except urllib.error.URLError as e:
            print("Poster download error:", e)
            return None

        pil_image = Image.open(io.BytesIO(raw_data)).convert('RGB')
        pil_image = pil_image.resize((POSTER_WIDTH, POSTER_HEIGHT))

        wx_image = wx.Image(POSTER_WIDTH, POSTER_HEIGHT)
        wx_image.SetData(pil_image.tobytes())
        return wx_image.ConvertToBitmap()


    def OnSelectMovie(self, event):
        index = event.GetIndex()
        movie = self.displayed[index]
        bitmap = self._load_poster(movie.poster_url)
        if bitmap is None:
            self.poster.SetBitmap(wx.Bitmap(POSTER_WIDTH, POSTER_HEIGHT))  # празно
        else:
            self.poster.SetBitmap(bitmap)

    def OnSearch(self, event):
        title = self.search_input.GetValue().strip()
        if not title:
            self.result_label.SetLabel('Въведи заглавие.')
            return

        movie = self.api.search_by_title(title)
        if movie is None:
            self.found_movie = None
            self.result_label.SetLabel('Филмът не е намерен (или няма интернет).')
        else:
            self.found_movie = movie
            self.result_label.SetLabel(
                f'Намерен: {movie.title} ({movie.year}) - {movie.genre}')

    def OnAdd(self, event):
        if self.found_movie is None:
            self.result_label.SetLabel('Първо потърси филм.')
            return

        added = self.catalog.add_movie(self.found_movie)
        if added:
            self.db.add_movie(self.found_movie)
            self.refresh_list()
            self.result_label.SetLabel(f'Добавен: {self.found_movie.title}')
        else:
            self.result_label.SetLabel('Този филм вече е в каталога.')

    def OnDelete(self, event):
        movie = self.get_selected_movie()
        if movie is None:
            return
        self.catalog.remove_movie(movie.imdb_id)
        self.db.delete_movie(movie.imdb_id)
        self.refresh_list()
        self.result_label.SetLabel(f'Изтрит: {movie.title}')

    def OnToggleWatched(self, event):
        movie = self.get_selected_movie()
        if movie is None:
            return
        movie.watched = not movie.watched
        self.db.add_movie(movie)
        self.refresh_list()

    def OnRate(self, event):
        movie = self.get_selected_movie()
        if movie is None:
            return
        try:
            rating = int(self.rating_input.GetValue())
        except ValueError:
            self.result_label.SetLabel('Оценката трябва да е число.')
            return
        if rating < 1 or rating > 10:
            self.result_label.SetLabel('Оценката трябва да е между 1 и 10.')
            return

        movie.user_rating = rating
        self.db.add_movie(movie)
        self.refresh_list()
        self.result_label.SetLabel(f'Оценен: {movie.title} -> {rating}')

    def OnRecommend(self, event):
        recommender = Recommender(self.catalog)
        movies = recommender.recommend()
        if not movies:
            self.rec_label.SetLabel(
                'Няма препоръки. Маркирай филми като гледани или ги оцени.')
            return
        names = '\n'.join(f'- {m.title} ({m.year}) [{m.genre}]' for m in movies)
        self.rec_label.SetLabel('Препоръчани за теб:\n' + names)

    def OnClose(self, event):
        self.db.close()
        self.Close()


def main():
    app = wx.App()
    MovieVaultFrame()
    app.MainLoop()


if __name__ == '__main__':
    main()