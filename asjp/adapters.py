from __future__ import unicode_literals
from tempfile import mkdtemp
from shutil import rmtree
import os

from sqlalchemy.orm import joinedload_all

from clld.util import binary_type
from clld.db.meta import DBSession
from clld.db.models.common import ValueSet, Language, Parameter, Dataset
from clld.web.adapters.base import Representation, Index
from clld.web.adapters.geojson import GeoJsonLanguages, pacific_centered_coordinates
from clld.web.adapters.download import Download
from clld.interfaces import ILanguage, IIndex
from clld.web.maps import SelectedLanguagesMap, GeoJsonSelectedLanguages
from clld.lib.dsv import UnicodeWriter

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


class Tab(Download):
    ext = 'tab'

    fields = [
        ('names', lambda l: l.id),
        ('wls_fam', lambda l: l.classification_wals.split('.')[0]
            if '.' in l.classification_wals else ''),
        ('wls_gen', lambda l: l.classification_wals.split('.')[1]
            if '.' in l.classification_wals else ''),
        ('e', lambda l: l.classification_ethnologue),
        ('hh', lambda l: l.classification_glottolog),
        ('lat', lambda l: l.latitude),
        ('lon', lambda l: l.longitude),
        ('pop', lambda l: l.number_of_speakers),
        ('wcode', lambda l: ''),
        ('iso', lambda l: l.code_iso),
    ]

    def create(self, req, filename=None, verbose=True):  # pragma: no cover
        meanings = [(p.name, p.id)
                    for p in DBSession.query(Parameter).order_by(Parameter.pk)]
        tmp = mkdtemp()
        path = os.path.join(tmp, 'asjp.tab')
        with UnicodeWriter(f=path, delimiter=binary_type("\t")) as writer:
            writer.writerow([f[0] for f in self.fields] + [m[0] for m in meanings])
            for lang in DBSession.query(Doculect).order_by(Doculect.pk).options(
                    joinedload_all(Language.valuesets, ValueSet.values),
                    joinedload_all(Language.valuesets, ValueSet.parameter)
            ).limit(10000):
                row = [f[1](lang) for f in self.fields]
                vss = {vs.parameter.id: vs for vs in lang.valuesets}
                row.extend([Doculect.format_words(vss.get(m[1])) for m in meanings])
                writer.writerow(row)
        Download.create(self, req, filename=path)
        rmtree(tmp)


def includeme(config):
    config.register_adapter(GeoJsonAllLanguages, ILanguage, IIndex)
    config.register_adapter(Wordlists, ILanguage, IIndex)
    config.register_adapter(Wordlist, ILanguage)
    config.register_adapter(MapView, ILanguage, IIndex)
    config.register_download(Tab(Dataset, 'asjp'))
