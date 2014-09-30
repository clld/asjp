from __future__ import unicode_literals

from sqlalchemy.orm import joinedload_all
from clld.db.meta import DBSession
from clld.db.models.common import ValueSet, Language
from clld.web.adapters.base import Representation, Index
from clld.web.adapters.geojson import GeoJsonLanguages, pacific_centered_coordinates
from clld.interfaces import ILanguage, IIndex
from clld.web.maps import SelectedLanguagesMap, GeoJsonSelectedLanguages

from asjp.models import txt_header, Doculect


class _Language(object):
    def __init__(self, pk, name, longitude, latitude, id_):
        self.pk = pk
        self.name = name
        self.longitude = longitude
        self.latitude = latitude
        self.id = id_

    def __json__(self, req):
        return self.__dict__


class GeoJsonAllLanguages(GeoJsonLanguages):
    def feature_iterator(self, ctx, req):
        for row in DBSession.query(
            Language.pk, Language.name, Language.longitude, Language.latitude, Language.id
        ):
            yield _Language(*row)

    def get_coordinates(self, language):
        return pacific_centered_coordinates(language)


class Wordlist(Representation):
    mimetype = str('text/plain')
    extension = str('txt')

    def render(self, ctx, req):
        return ctx.to_txt()


class Wordlists(Index):
    extension = str('txt')
    mimetype = str('text/plain')

    def render(self, ctx, req):
        res = [txt_header()]

        #
        # TODO: render warning, if more than 1500 items would have matched.
        #
        ids = [d.pk for d in ctx.get_query(limit=1500)]

        q = DBSession.query(Doculect)\
            .filter(Doculect.pk.in_(ids))\
            .options(
                joinedload_all(Language.valuesets, ValueSet.values),
                joinedload_all(Language.valuesets, ValueSet.parameter))

        for wordlist in q:
            res.append(wordlist.to_txt())

        return '\n'.join(res)


class _GeoJsonSelectedLanguages(GeoJsonSelectedLanguages):
    def get_coordinates(self, language):
        return pacific_centered_coordinates(language)


class MapView(Index):
    extension = str('map.html')
    mimetype = str('text/vnd.clld.map+html')
    send_mimetype = str('text/html')
    template = 'language/map_html.mako'

    def template_context(self, ctx, req):
        languages = list(ctx.get_query(limit=8000))
        return {
            'map': SelectedLanguagesMap(
                ctx, req, languages, geojson_impl=_GeoJsonSelectedLanguages),
            'languages': languages}


def includeme(config):
    config.register_adapter(GeoJsonAllLanguages, ILanguage, IIndex)
    config.register_adapter(Wordlists, ILanguage, IIndex)
    config.register_adapter(Wordlist, ILanguage)
    config.register_adapter(MapView, ILanguage, IIndex)
