from __future__ import unicode_literals

from clld.db.meta import DBSession
from clld.db.models.common import ValueSet, Language
from clld.web.adapters.geojson import GeoJsonParameter, GeoJsonLanguages, pacific_centered_coordinates
from clld.interfaces import IParameter, ILanguage, IIndex


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


def includeme(config):
    config.register_adapter(GeoJsonMeaning, IParameter)
    config.register_adapter(GeoJsonAllLanguages, ILanguage, IIndex)
