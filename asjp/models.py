from zope.interface import implementer
from sqlalchemy import (
    Column,
    String,
    Unicode,
    Integer,
    Boolean,
    ForeignKey,
)
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql.expression import cast, true

from clld import interfaces
from clld.db.meta import CustomModelMixin, DBSession
from clld.db.models.common import (
    Value,
    Contribution,
    Language,
    ValueSet,
    Parameter,
)
from pyasjp.models import ASJPCODES


def asjp_name(name):
    if '"' in name:
        name = name.split('"')[1]
    return name.replace("'", "").replace(" ", "_").replace("/", "_").upper()


def txt_header(synonyms=2, words=28, year=1700, session=None):
    """
     2    28  1700     3
(I4,20X,10A1)
    """
    session = session or DBSession
    rjust = lambda n, s=6: str(n).rjust(s)

    lines = [
        '%s%s%s%s' % tuple(map(rjust, (synonyms, words, year, 3))),
        '(I4,20X,10A1)']

    for meaning in DBSession.query(Meaning)\
            .filter(Meaning.core == true())\
            .order_by(cast(Meaning.id, Integer)):
        lines.append('%s%s%s' % (rjust(int(meaning.id), 4), 20 * ' ', meaning.name))

    lines.append('')
    for char in ASJPCODES:
        lines.append(char)
    lines.append('')
    lines.append('')
    return '\n'.join(lines)


# -----------------------------------------------------------------------------
# specialized common mapper classes
# -----------------------------------------------------------------------------
@implementer(interfaces.IParameter)
class Meaning(CustomModelMixin, Parameter):
    pk = Column(Integer, ForeignKey('parameter.pk'), primary_key=True)
    core = Column(Boolean, default=False)
    concepticon_id = Column(Unicode)
    concepticon_gloss = Column(Unicode)


@implementer(interfaces.IValue)
class Word(CustomModelMixin, Value):
    pk = Column(Integer, ForeignKey('value.pk'), primary_key=True)
    loan = Column(Boolean, default=False)


@implementer(interfaces.IValueSet)
class Synset(CustomModelMixin, ValueSet):
    pk = Column(Integer, ForeignKey('valueset.pk'), primary_key=True)
    words = Column(Unicode)


@implementer(interfaces.ILanguage)
class Doculect(CustomModelMixin, Language):
    pk = Column(Integer, ForeignKey('language.pk'), primary_key=True)
    wordlist_pk = Column(Integer, ForeignKey('contribution.pk'))
    wordlist = relationship(Contribution, backref=backref('language', uselist=False))
    code_wals = Column(String)
    code_iso = Column(String)
    code_glottolog = Column(String)
    classification_wals = Column(Unicode)
    classification_ethnologue = Column(Unicode)
    classification_glottolog = Column(Unicode)
    number_of_speakers = Column(Integer)
    recently_extinct = Column(Boolean, default=False)
    long_extinct = Column(Boolean, default=False)
    year_of_extinction = Column(Integer)
    txt = Column(Unicode)

    wals_genus = Column(String)
    wals_family = Column(String)
    ethnologue_family = Column(Unicode)
    glottolog_family = Column(Unicode)

    def href(self, type):
        if type == 'wals_genus' and self.wals_genus:
            return 'https://wals.info/languoid/genus/' + self.wals_genus

        if type == 'wals_family' and self.wals_family:
            return 'https://wals.info/languoid/family/' + self.wals_family

        if type == 'wals' and self.code_wals:
            return 'https://wals.info/languoid/lect/wals_code_' + self.code_wals

        if type == 'glottolog' and self.code_glottolog:
            return 'https://glottolog.org/resource/languoid/id/' + self.code_glottolog
