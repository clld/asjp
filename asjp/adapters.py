from clld.db.meta import DBSession
from clld.db.models.common import Language
from clld.web.adapters.base import Representation, Index
from clld.web.adapters.geojson import GeoJsonLanguages
from clld.interfaces import ILanguage, IIndex
from clld.web.maps import SelectedLanguagesMap

from asjp.models import txt_header


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


class Wordlist(Representation):
    """The ASJP wordlist format suitable as input for the ASJP software.
    """
    name = "ASJP text format"
    mimetype = str('text/plain')
    extension = str('txt')

    def render(self, ctx, req):
        return ctx.txt


class Wordlists(Index):
    name = "ASJP text format (only up to 1500 wordlists can be exported)"
    extension = str('txt')
    mimetype = str('text/plain')

    def render(self, ctx, req):
        res = [txt_header()]
        for d in ctx.get_query(limit=10000):
            res.append(d.txt)
        res.append('')
        res.append('')
        return '\n'.join(res)


class MapView(Index):
    extension = str('map.html')
    mimetype = str('text/vnd.clld.map+html')
    send_mimetype = str('text/html')
    template = 'language/map_html.mako'

    def template_context(self, ctx, req):
        languages = list(ctx.get_query(limit=8000))
        return {
            'map': SelectedLanguagesMap(ctx, req, languages),
            'languages': languages}


def includeme(config):
    config.register_adapter(GeoJsonAllLanguages, ILanguage, IIndex)
    config.register_adapter(Wordlists, ILanguage, IIndex)
    config.register_adapter(Wordlist, ILanguage)
    config.register_adapter(MapView, ILanguage, IIndex)
