# coding: utf-8
from __future__ import unicode_literals
import re

from zope.interface import implementer
from sqlalchemy import (
    Column,
    String,
    Unicode,
    Integer,
    Boolean,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.sql.expression import cast

from clld import interfaces
from clld.db.meta import Base, CustomModelMixin, DBSession
from clld.db.models.common import (
    Value,
    Contribution,
    Language,
    ValueSet,
    Parameter,
    Identifier,
    LanguageIdentifier,
    IdentifierType,
)

# see
# Brown, Cecil H., Eric W. Holman, Søren Wichmann, and Viveka Vilupillai. 2008.
# Automated classification of the world’s languages:
# a description of the method and preliminary results.
# STUF – Language Typology and Universals 61:285-308.
ASJPCODES = 'pbfvmw8tdszcnrlSZCjT5ykgxNqXh7L4G!ieE3auo'

MEANINGS = {
    1: 'I',
    2: 'you',
    3: 'we',
    11: 'one',
    12: 'two',
    18: 'person',
    19: 'fish',
    21: 'dog',
    22: 'louse',
    23: 'tree',
    25: 'leaf',
    28: 'skin',
    30: 'blood',
    31: 'bone',
    34: 'horn',
    39: 'ear',
    40: 'eye',
    41: 'nose',
    43: 'tooth',
    44: 'tongue',
    47: 'knee',
    48: 'hand',
    51: 'breast',
    53: 'liver',
    54: 'drink',
    57: 'see',
    58: 'hear',
    61: 'die',
    66: 'come',
    72: 'sun',
    74: 'star',
    75: 'water',
    77: 'stone',
    82: 'fire',
    85: 'path',
    86: 'mountain',
    92: 'night',
    95: 'full',
    96: 'new',
    100: 'name',
}

MEANINGS_NON_CORE = {
    4: 'this',
    5: 'that',
    6: 'who',
    7: 'what',
    8: 'not',
    9: 'all',
    10: 'many',
    13: 'big',
    14: 'long',
    15: 'small',
    16: 'woman',
    17: 'man',
    20: 'bird',
    24: 'seed',
    26: 'root',
    27: 'bark',
    29: 'flesh',
    32: 'grease',
    33: 'egg',
    35: 'tail',
    36: 'feather',
    37: 'hair',
    38: 'head',
    42: 'mouth',
    45: 'claw',
    46: 'foot',
    49: 'belly',
    50: 'neck',
    52: 'heart',
    55: 'eat',
    56: 'bite',
    59: 'know',
    60: 'sleep',
    62: 'kill',
    63: 'swim',
    64: 'fly',
    65: 'walk',
    67: 'lie',
    68: 'sit',
    69: 'stand',
    70: 'give',
    71: 'say',
    73: 'moon',
    76: 'rain',
    78: 'sand',
    79: 'earth',
    80: 'cloud',
    81: 'smoke',
    83: 'ash',
    84: 'burn',
    87: 'red',
    88: 'green',
    89: 'yellow',
    90: 'white',
    91: 'black',
    93: 'hot',
    94: 'cold',
    97: 'good',
    98: 'round',
    99: 'dry',
}

MEANINGS_ALL = {}
MEANINGS_ALL.update(MEANINGS)
MEANINGS_ALL.update(MEANINGS_NON_CORE)

LANGUAGE_LINE_PATTERN = re.compile(
    '(?P<name>[^\{]+)\{(?P<w>[^\|]*)\|(?P<e>[^\@]*)\@(?P<g>[^\}]*)\}?')


def parse_metadata(line):
    """
    The second line gives properties of the languages, in fixed format separated by blanks
    (not tabs), so the columns are important.

    Col. 2: 3 if the language is the first one in a new WALS family, 2 if it’s the first
    language in a new WALS genus, 1 otherwise.

    Col. 4-10, right justified: latitude in degrees and
    hundredths of a degree; minus means South.

    Col. 12-18, right justified: longitude in degrees a
    nd hundredths of a degree; minus means West.
    Latitudes and longitudes were ascertained from WALS, or from the maps in Ethnologue or
    Moseley and Asher (1994), or from information in the source for the list.

    Col. 19-30, right justified: number of speakers, from Ethnologue. This number always
    refers to the entire language, as defined in Ethnologue, even if the list itself
    refers to a dialect. The number is

        0 if the number of speakers is unknown;
        -1 if the language is recently extinct;
        -2 if the language is long extinct;
        or if the approximate date of extinction is known, the date is preceded by a minus
        sign.

    In the ASJP software, if there is a date in the first line of the entire file, lists
    with earlier extinction dates here are ignored, as are lists with -2; otherwise, all
    lists are read.

    Col. 34-36: three-letter WALS code, if any.

    Col. 40-42: three-letter ISO639-3 code, if any. This code is included for languages in
    previous editions of Ethnologue even if they aren’t in the 17th edition. Languages
    that lack an ISO639-3 code but can be placed in the Ethnologue classification are
    given a code consisting of two letters followed by the number 0 (for use in ASJP
    software).
    """
    lat = line[4:11].strip()
    lng = line[11:18].strip()
    nos = int(line[18:30].strip() or 0)
    return dict(
        latitude=float(lat) if lat else None,
        longitude=float(lng) if lng else None,
        number_of_speakers=nos if nos >= 0 else 0,
        recently_extinct=nos == -1 or nos < -2,
        long_extinct=nos == -2,
        year_of_extinction=abs(nos) if nos < -2 else None,
        code_wals=line[33:36].strip() or None,
        code_iso=line[39:42].strip() or None)


def parse_word(line):
    header, body = line.split('\t', 1)
    body = body.strip()
    comment = ''
    if re.search('  | //', body):
        body, comment = re.split('  | //', body, 1)
    comment = comment.strip()
    words = []
    for word in body.split(','):
        word = word.strip()
        if word != 'XXX':
            if word.startswith('%'):
                words.append((word[1:], True))
            else:
                words.append((word, False))
    number = header.split()[0]
    if number.endswith('.'):
        number = number[:-1].strip()
    return str(int(number)), words, comment or None


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
            .filter(Meaning.core == True)\
            .order_by(cast(Meaning.id, Integer)):
        lines.append('%s%s%s' % (rjust(int(meaning.id), 4), 20 * ' ', meaning.name))

    lines.append('')
    for char in ASJPCODES:
        lines.append(char)
    lines.append('')
    return '\n'.join(lines)


#-----------------------------------------------------------------------------
# specialized common mapper classes
#-----------------------------------------------------------------------------
@implementer(interfaces.IParameter)
class Meaning(Parameter, CustomModelMixin):
    pk = Column(Integer, ForeignKey('parameter.pk'), primary_key=True)
    core = Column(Boolean, default=False)


@implementer(interfaces.IValue)
class Word(Value, CustomModelMixin):
    pk = Column(Integer, ForeignKey('value.pk'), primary_key=True)
    loan = Column(Boolean, default=False)


@implementer(interfaces.ILanguage)
class Doculect(Language, CustomModelMixin):
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

    @classmethod
    def from_txt(cls, txt, session=None, **kw):
        session = session or DBSession

        lines = filter(None, txt.split('\n'))
        m = LANGUAGE_LINE_PATTERN.match(lines[0])
        assert m
        kw['id'] = m.group('name')
        kw['name'] = ' '.join(s.capitalize() for s in kw['id'].split('_'))
        for cname in ['wals', 'ethnologue', 'glottolog']:
            if m.group(cname[0]):
                kw['classification_' + cname] = m.group(cname[0])

        kw.update(parse_metadata(lines[1]))
        doculect = cls(**kw)

        doculect.wordlist = Contribution(
            id=kw['id'], language=doculect, name=doculect.id)

        for line in lines[2:]:
            if '\t' in line:
                wid, words, comment = parse_word(line)
                #if int(wid) not in MEANINGS_ALL:
                #    # drop non-core meanings
                #    continue
                vsid = '%s-%s' % (doculect.id, wid)
                vs = ValueSet(
                    id=vsid,
                    description=comment,
                    language=doculect,
                    contribution=doculect.wordlist,
                    parameter=Parameter.get(wid, session=session))

                for i, word in enumerate(words):
                    id_ = '%s-%s' % (vsid, i + 1)
                    word, loan = word
                    word = Word(id=id_, name=word, valueset=vs, loan=loan)

        return doculect

    def to_txt(self):
        """render the wordlist in the ASJP plain text format.
        """
        nos = self.number_of_speakers
        if self.year_of_extinction:
            nos = -self.year_of_extinction
        elif self.recently_extinct:
            nos = -1
        elif self.long_extinct:
            nos = -2
        lines = [
            '%s{%s|%s|@%s}' % (
                self.id,
                self.classification_wals or '',
                self.classification_ethnologue or '',
                self.classification_glottolog or ''),
            '%s%s%s%s%s%s' % (
                '1'.rjust(2),
                ('' if self.latitude is None else ('%.2f' % self.latitude)).rjust(8),
                ('' if self.longitude is None else ('%.2f' % self.longitude)).rjust(8),
                str(nos).rjust(12),
                (self.code_wals or '').rjust(6),
                (self.code_iso or '').rjust(6))]
        format_word = lambda w: '%' + w.name if w.loan else w.name
        for synset in sorted(self.valuesets, key=lambda item: int(item.parameter.id)):
            lines.append('%s %s\t%s //%s' % (
                synset.parameter.id,
                MEANINGS_ALL[int(synset.parameter.id)],
                ', '.join(map(
                    format_word, sorted(synset.values, key=lambda item: item.id))),
                (' ' + synset.description) if synset.description else ''))
        return '\n'.join(lines)
