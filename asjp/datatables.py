import re

from sqlalchemy import or_
from clld.web.datatables import Values, Sources
from clld.web.datatables.base import (
    Col, LinkCol, LinkToMapCol, IntegerIdCol,
)
from clld.web.datatables.language import Languages
from clld.web.util.helpers import external_link
from clld.db.models.common import Language, Parameter, Value

from asjp.models import Doculect, Word
from asjp.util import normalize_classification

from clld.web.util import concepticon


class ConcepticonCol(Col):
    __kw__ = dict(bSortable=False, bSearchable=False)

    def format(self, item):
        return concepticon.link(
            item.valueset.parameter.concepticon_id,
            label=item.valueset.parameter.concepticon_gloss)


class Words(Values):
    """Lists of words
    """
    def col_defs(self):
        res = []
        if self.parameter:
            res = [
                LinkCol(
                    self, 'language',
                    model_col=Language.name,
                    get_object=lambda i: i.valueset.language),
            ]
        elif self.language:
            res = [
                IntegerIdCol(
                    self, 'id',
                    input_size='mini',
                    model_col=Parameter.id,
                    get_object=lambda i: i.valueset.parameter),
                LinkCol(
                    self, 'meaning',
                    model_col=Parameter.name,
                    get_object=lambda i: i.valueset.parameter),
                ConcepticonCol(self, 'concepticon'),
            ]
        return res + [
            Col(self, 'name', sTitle='Word', model_col=Value.name),
            Col(self, 'loan', model_col=Word.loan),
        ]


class IsoCol(Col):
    __kw__ = dict(sTitle='ISO 639-3', input_size='mini')

    def search(self, qs):
        whitespace = re.compile('\s+')
        if whitespace.search(qs):
            return or_(*[
                Doculect.code_iso == q.strip() for q in whitespace.split(qs.lower())])
        return Col.search(self, qs)


class ExtLinkCol(Col):
    def __init__(self, dt, name, link_type, **kw):
        self.link_type = link_type
        Col.__init__(self, dt, name, **kw)

    def format(self, item):
        label = Col.format(self, item)
        href = item.href(self.link_type)
        if href:
            return external_link(href, label=label)
        return label


class YesNoCol(Col):
    __kw__ = dict(choices=[('True', 'yes'), ('False', 'no')])

    def format_value(self, value):
        return ['no', 'yes'][int(value)]


class Wordlists(Languages):
    def col_defs(self):
        return [
            LinkToMapCol(self, 'm'),
            LinkCol(self, 'name'),
            ExtLinkCol(self, 'glottocode', 'glottolog', model_col=Doculect.code_glottolog),
            IsoCol(self, 'iso', model_col=Doculect.code_iso),
            ExtLinkCol(
                self, 'wals', 'wals',
                sTitle='WALS', input_size='mini', model_col=Doculect.code_wals),
            Col(self, 'latitude', input_size='mini'),
            Col(self, 'longitude', input_size='mini'),
            YesNoCol(
                self, 'long_extinct',
                sTitle='Ancient', input_size='mini', model_col=Doculect.long_extinct),
            YesNoCol(
                self, 'recently_extinct',
                input_size='mini', model_col=Doculect.recently_extinct),
            Col(self, 'year_of_extinction',
                input_size='mini', model_col=Doculect.year_of_extinction),
            Col(self, 'classification_wals',
                sTitle='Classification WALS',
                format=lambda i: normalize_classification(i.classification_wals, 'wals'),
                model_col=Doculect.classification_wals),
            Col(self, 'classification_glottolog',
                sTitle='Classification Glottolog',
                format=lambda i: normalize_classification(i.classification_glottolog),
                model_col=Doculect.classification_glottolog),
        ]


class Refs(Sources):
    def col_defs(self):
        return Sources.col_defs(self)[:-1]


def includeme(config):
    config.register_datatable('values', Words)
    config.register_datatable('languages', Wordlists)
    config.register_datatable('sources', Refs)
