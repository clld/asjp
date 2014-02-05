from path import path

from clld.tests.util import TestWithApp

import asjp


class Tests(TestWithApp):
    __cfg__ = path(asjp.__file__).dirname().joinpath('..', 'development.ini').abspath()
    __setup_db__ = False

    def test_home(self):
        self.app.get('/', status=200)

    def test_meanings(self):
        self.app.get('/parameters?sEcho=1', xhr=True, status=200)
        self.app.get('/parameters', status=200)
        self.app.get('/parameters/1', status=200)

    def test_contributions(self):
        self.app.get('/contributions?sEcho=1', xhr=True, status=200)

    def test_wordlist(self):
        self.app.get('/languages?sEcho=1&sSearch_3=gwj+gnk', xhr=True, status=200)
        self.app.get('/languages.map.html?sEcho=1&sSearch_3=gwj', status=200)
        self.app.get('/languages.geojson?sEcho=1&sSearch_3=gwj', status=200)
        self.app.get('/languages.txt?sEcho=1&sSearch_3=gwj', status=200)
        self.app.get(
            '/languages/KICHEE_ALDEA_ARGUETA_SOLOLA.txt?sEcho=1&sSearch_3=gwj',
            status=200)

    def test_words(self):
        self.app.get(
            '/values?sEcho=1&language=KICHEE_ALDEA_ARGUETA_SOLOLA', xhr=True, status=200)
        self.app.get('/values?sEcho=1&parameter=1', xhr=True, status=200)
