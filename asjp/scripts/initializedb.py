# coding: utf8
from __future__ import unicode_literals, print_function
import sys
import re

from sqlalchemy import create_engine
from sqlalchemy.orm import joinedload_all
from clld.scripts.util import initializedb, Data, glottocodes_by_isocode
from clld.db.meta import DBSession
from clld.db.models import common
from clldutils.misc import slug
from clld.lib.bibtex import EntryType

import asjp
from asjp import models
from asjp.scripts.util import parse_meta, get_transcriber_map


def parse(fp):
    wordlist = None

    for line in fp:
        m = models.LANGUAGE_LINE_PATTERN.match(line)
        if m:
            if wordlist:
                yield wordlist
            wordlist = [line]
        else:
            if wordlist:
                wordlist.append(line)

    if wordlist:
        yield wordlist


def add_codes(lang):
    for attr, prefix in dict(wals='wals_code_', iso='', glottolog='').items():
        code = getattr(lang, 'code_' + attr)
        if code:
            if attr == 'iso' and not re.match('[a-z]{3}$', code):
                continue
            id_ = prefix + code
            identifier = common.Identifier.get(id_, default=None)
            if not identifier:
                identifier = common.Identifier(
                    id=id_,
                    name=code,
                    type=getattr(common.IdentifierType, attr).value)
            common.LanguageIdentifier(identifier=identifier, language=lang)


def get_source(source, id_):
    author, year, description = source

    url = None
    match = re.search('(?P<url>http(s)?://[^\s]+)(\s+|$)', description)
    if match:
        url = match.group('url')

    res = common.Source(
        id='%s' % id_,
        name='%s %s' % (author or 'n.a.', year or 'n.d.'),
        description=description,
        author=author,
        year=year,
        title=description,
        url=url,
        bibtex_type=EntryType.misc)
    DBSession.add(res)
    return res


def main(args):
    meta = parse_meta(args)
    sources = {}
    for m in meta.values():
        for s in m.sources:
            sources[s] = None
    for i, s in enumerate(sources):
        sources[s] = get_source(s, i + 1)

    glottocodes = glottocodes_by_isocode('postgresql://robert@/glottolog3')

    data = Data()

    wals = create_engine('postgresql://robert@/wals3')
    wals_families = {}
    for row in wals.execute('select name, id from family'):
        wals_families[row[0]] = row[1]
        wals_families[row[1]] = row[1]

    #for item in reader(args.data_file('WALSFamilyAbbreviations.tab'), namedtuples=True, encoding='latin1'):
    #    name = item.FAMILY
    #    if name not in wals_families:
    #        name = slug(name)
    #        if name not in wals_families:
    #            print('missing wals family:', item.FAMILY)
    #            name = None
    #    if name:
    #        wals_families[item.ABBREVIATION] = wals_families[name]

    wals_genera = {row[0]: row[0] for row in wals.execute('select id from genus')}

    with args.data_file('listss18.txt').open(encoding='latin1') as fp:
        wordlists = ['\n'.join(lines) for lines in parse(fp)]

    dataset = common.Dataset(
        id=asjp.__name__,
        name="The ASJP Database",
        contact="wichmannsoeren@gmail.com",
        description="The Automated Similarity Judgment Program",
        domain='asjp.clld.org',
        publisher_name="Max Planck Institute for the Science of Human History",
        publisher_place="Jena",
        publisher_url="https://www.shh.mpg.de",
        license='http://creativecommons.org/licenses/by/4.0/',
        jsondata={
            'license_icon': 'cc-by.png',
            'license_name': 'Creative Commons Attribution 4.0 International License'})
    DBSession.add(dataset)

    transcribers = get_transcriber_map(args)
    for i, spec in enumerate([
        ('SW', "Søren Wichmann"),
        ('AM', "André Müller"),
        ('AKW', "Annkathrin Wett"),
        ('VV', "Viveka Velupillai"),
        ('JB', "Julia Bischoffberger"),
        ('CB', "Cecil H. Brown"),
        ('EH', "Eric W. Holman"),
        ('SS', "Sebastian Sauppe"),
        ('ZM', "Zarina Molochieva"),
        ('PB', "Pamela Brown"),
        ('HH', "Harald Hammarström"),
        ('OB', "Oleg Belyaev"),
        ('JML', "Johann-Mattis List"),
        ('DBA', "Dik Bakker"),
        ('DE', "Dmitry Egorov"),
        ('MU', "Matthias Urban"),
        ('RM', "Robert Mailhammer"),
        ('AC', "Agustina Carrizo"),
        ('MSD', "Matthew S. Dryer"),
        ('EK', "Evgenia Korovina"),
        ('DB', "David Beck"),
        ('HG', "Helen Geyer"),
        ('PE', "Patience Epps"),
        ('AG', "Anthony Grant"),
        ('PS', "Paul Sidwell"),  # not in citation
        ('KTR', "K. Taraka Rama"),  # not in citation
        ('PV', "Pilar Valenzuela"),
        ('MD', "Mark Donohue"),  # not in citation
    ]):
        id_, name = spec
        if id_ in transcribers:
            assert name == transcribers.pop(id_)
        contributor = data.add(common.Contributor, id_, id=id_, name=name)
        if id_ in ['SW', 'EH', 'CB']:
            DBSession.add(common.Editor(
                dataset=dataset,
                ord=i + 1,
                contributor=contributor))
    for id_, name in transcribers.items():
        data.add(common.Contributor, id_, id=id_, name=name)

    for id_ in sorted(models.MEANINGS_ALL.keys()):
        data.add(
            models.Meaning, id_,
            id=str(id_), name=models.MEANINGS_ALL[id_], core=id_ in models.MEANINGS)

    for n, l in enumerate(wordlists):
        #if n > 100:
        #    break
        lang = models.Doculect.from_txt(l)
        if lang.classification_wals:
            family, genus = lang.classification_wals.split('.')
            lang.wals_family = wals_families.get(family)
            lang.wals_genus = wals_genera.get(slug(genus))
        lang.code_glottolog = glottocodes.get(lang.code_iso)
        add_codes(lang)
        data.add(models.Doculect, lang.id, _obj=lang)
        DBSession.flush()
        md = meta.pop(lang.id, None)
        assert md
        # associate transcribers and sources
        for i, transcriber in enumerate(md.transcribers):
            common.ContributionContributor(
                contribution=lang.wordlist,
                contributor=data['Contributor'][transcriber],
                ord=i + 1)
        for source in md.sources:
            DBSession.add(
                common.LanguageSource(language_pk=lang.pk, source_pk=sources[source].pk))

    print(list(meta.keys()))


def prime_cache(args):
    """If data needs to be denormalized for lookup, do that here.
    This procedure should be separate from the db initialization, because
    it will have to be run periodiucally whenever data has been updated.
    """
    q = DBSession.query(models.Doculect)\
        .order_by(models.Doculect.pk)\
        .options(
            joinedload_all(common.Language.valuesets, common.ValueSet.values),
            joinedload_all(common.Language.valuesets, common.ValueSet.parameter)
        )
    for doculect in q:
        doculect.txt = doculect.to_txt()

    #previous = None
    #for doculect in page_query(q, n=100, verbose=True, commit=True):
    #    doculect.txt = doculect.to_txt(previous=previous)
    #    previous = doculect

    #
    # TODO: include macroarea info from glottolog!
    #


if __name__ == '__main__':
    initializedb(create=main, prime_cache=prime_cache)
    sys.exit(0)
