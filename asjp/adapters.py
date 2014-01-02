from __future__ import unicode_literals

from sqlalchemy.orm import joinedload_all
from clld.db.meta import DBSession
from clld.db.models.common import ValueSet, Language
from clld.web.adapters.base import Representation, Index
from clld.web.adapters.geojson import GeoJsonParameter, GeoJsonLanguages, pacific_centered_coordinates
from clld.interfaces import IParameter, ILanguage, IIndex

from asjp.models import txt_header, Doculect


class GeoJsonMeaning(GeoJsonParameter):
    def feature_iterator(self, ctx, req):
        languages = DBSession.query(ValueSet.language_pk)\
            .filter(ValueSet.parameter_pk == ctx.pk).subquery()
        return DBSession.query(Language)\
            .filter(Language.pk.in_(languages))

    def get_language(self, ctx, req, language):
        return language

    def feature_properties(self, ctx, req, language):
        return {}

    def get_coordinates(self, language):
        return pacific_centered_coordinates(language)


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
        # TODO: render warning, if more than 1000 items would have matched.
        #
        ids = [d.pk for d in ctx.get_query(limit=1000)]

        q = DBSession.query(Doculect)\
            .filter(Doculect.pk.in_(ids))\
            .options(
                joinedload_all(Language.valuesets, ValueSet.values),
                joinedload_all(Language.valuesets, ValueSet.parameter))

        for wordlist in q:
            res.append(wordlist.to_txt())

        return '\n'.join(res)


def includeme(config):
    config.register_adapter(GeoJsonMeaning, IParameter)
    config.register_adapter(GeoJsonAllLanguages, ILanguage, IIndex)
    config.register_adapter(Wordlists, ILanguage, IIndex)
    config.register_adapter(Wordlist, ILanguage)
