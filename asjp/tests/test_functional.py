from path import path

from clld.tests.util import TestWithApp

import asjp


class Tests(TestWithApp):
    __cfg__ = path(asjp.__file__).dirname().joinpath('..', 'development.ini').abspath()
    __setup_db__ = False

    def test_home(self):
        self.app.get_html('/')

    def test_meanings(self):
        self.app.get_dt('/parameters')
        self.app.get_html('/parameters')
        self.app.get_html('/parameters/1')

    def test_contributions(self):
        self.app.get_dt('/contributions')

    def test_wordlist(self):
        self.app.get_dt('/languages?sSearch_3=gwj+gnk')
        self.app.get_html('/languages.map.html?sEcho=1&sSearch_3=gwj')
        self.app.get_json('/languages.geojson?sEcho=1&sSearch_3=gwj')
        self.app.get('/languages.txt?sEcho=1&sSearch_3=gwj')
        self.app.get('/languages/KICHEE_ALDEA_ARGUETA_SOLOLA.txt?sEcho=1&sSearch_3=gwj')

    def test_words(self):
        self.app.get_dt('/values?language=KICHEE_ALDEA_ARGUETA_SOLOLA')
        self.app.get_dt('/values?parameter=1')
