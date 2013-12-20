# coding: utf8
from __future__ import unicode_literals
import sys
import codecs
import json
import re

from sqlalchemy import create_engine
from clld.scripts.util import initializedb, Data
from clld.db.meta import DBSession
from clld.db.models import common

import asjp
from asjp import models
from asjp.scripts.util import parse, MEANINGS, parse_sources, asjp_name


GC = create_engine('postgresql://robert@/glottolog3')

glottocodes = {}
for row in GC.execute('select ll.hid, l.id from language as l, languoid as ll where ll.pk = l.pk'):
    if row[0] and len(row[0]) == 3:
        glottocodes[row[0]] = row[1]


def add_codes(data, l, isostring):
    if not isostring:
        return

    if isostring in data['Identifier']:
        iso = data['Identifier'][isostring]
    else:
        iso = data.add(
            common.Identifier, isostring,
            id=isostring, type=common.IdentifierType.iso.value, name=isostring)
    DBSession.add(common.LanguageIdentifier(identifier=iso, language=l))

    if isostring in glottocodes:
        gc = glottocodes[isostring]
        if gc in data['Identifier']:
            gc = data['Identifier'][gc]
        else:
            gc = data.add(
                common.Identifier, gc,
                id=gc, type=common.IdentifierType.glottolog.value, name=gc)
        DBSession.add(common.LanguageIdentifier(identifier=gc, language=l))


def main(args):
    sources = args.data_file('sources.json')
    if sources.exists():
        sources = json.load(open(sources))
    else:
        res = list(parse_sources(args))
        with open(sources, 'w') as fp:
            json.dump(res, fp)
        sources = res

    data = Data()

    dataset = common.Dataset(
        id=asjp.__name__,
        name="ASJP",
        contact="wichmann@eva.mpg.de",
        description="The Automated Similarity Judgement Program",
        domain='asjp.clld.org',
        license='http://creativecommons.org/licenses/by/3.0/',
        jsondata={
            'license_icon': 'cc-by.png',
            'license_name': 'Creative Commons Attribution 3.0 Unported License'})
    DBSession.add(dataset)

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
        ('DB', "Dik Bakker"),
        ('DE', "Dmitry Egorov"),
        ('MU', "Matthias Urban"),
        ('RM', "Robert Mailhammer"),
        ('AC', "Agustina Carrizo"),
        ('MSD', "Matthew S. Dryer"),
        ('EK', "Evgenia Korovina"),
        ('DBE', "David Beck"),
        ('HG', "Helen Geyer"),
        ('PE', "Pattie Epps"),
        ('AG', "Anthony Grant"),
        ('PS', "Paul Sidwell"),
        ('KTR', "K. Taraka Rama"),
        ('PV', "Pilar Valenzuela"),
        ('MD', "Mark Donohue"),
    ]):
        contributor = data.add(common.Contributor, spec[0], id=spec[0], name=spec[1])
        DBSession.add(common.Editor(dataset=dataset, ord=i + 1, contributor=contributor))

    for id_ in sorted(MEANINGS.keys()):
        data.add(common.Parameter, id_, id=str(id_), name=MEANINGS[id_])

    with codecs.open(args.data_file('listss16.txt'), encoding='latin1') as fp:
        wordlists = list(parse(fp))

    # keep a mapping of iso codes to wordlists to associate sources lateron
    langs_by_iso_code = {}

    for l in wordlists:
        if l['name'] in data['Language']:
            lang = data['Language'][l['name']]
            if lang.latitude != l['latitude'] or lang.longitude != l['longitude']:
                print l['name'], l['contribution']
                continue
        else:
            lang = data.add(
                common.Language, l['name'],
                id=l['name'],
                name=' '.join(s.capitalize() for s in l['name'].split('_')),
                latitude=l['latitude'],
                longitude=l['longitude'],
                jsondata=dict(number_of_speakers=l['population']))
            add_codes(data, lang, l['iso'])
            #
            # TODO: add WALS identifier!?
            #

        contrib = data.add(
            models.Wordlist, l['contribution'],
            id=l['contribution'],
            language=lang,
            name=l['contribution'] + ' wordlist')

        if l['iso']:
            if l['iso'] in langs_by_iso_code:
                langs_by_iso_code[l['iso']].append(lang)
            else:
                langs_by_iso_code[l['iso']] = [lang]

        for wid, wdata in l['words'].items():
            words, comment = wdata
            vsid = '%s-%s' % (l['contribution'], wid)
            vs = data.add(
                common.ValueSet, vsid,
                id=vsid,
                description=comment,
                language=lang,
                contribution=contrib,
                parameter=data['Parameter'][wid])

            for i, word in enumerate(words):
                id_ = '%s-%s' % (vsid, i + 1)
                word, loan = word
                data.add(models.Word, id_, id=id_, name=word, valueset=vs, loan=loan)

    ls = {}
    cc = {}
    for i, source in enumerate(sources):
        contributors = []
        for contributor in re.split('\s*/\s*|,\s*|\s+and\s+', source.get('author', '')):
            contributor = contributor.strip()
            if contributor:
                if not contributor in data['Contributor']:
                    print '---missing---', contributor, '--source--', source
                else:
                    contributors.append(data['Contributor'][contributor])
        if source['source'] in data['Source']:
            s = data['Source'][source['source']]
        else:
            s = data.add(common.Source, source['source'], id=str(i + 1), name=source['source'])

        langs = []
        if source.get('asjp_name') in data['Language']:
            langs = [data['Language'][source['asjp_name']]]
            #.sources.append(s)
        elif source.get('iso') in langs_by_iso_code:
            langs = langs_by_iso_code[source['iso']]
        elif source.get('name') and asjp_name(source.get('name', '')) in data['Language']:
            langs = [data['Language'][asjp_name(source['name'])]]
        for lang in set(langs):
            if (lang.id, s.id) not in ls:
                lang.sources.append(s)
                ls[(lang.id, s.id)] = 1
            for contribution in lang.wordlists:
                for contributor in set(contributors):
                    if (contributor.id, contribution.id) not in cc:
                        DBSession.add(common.ContributionContributor(
                            contribution=contribution,
                            contributor=contributor))
                        cc[(contributor.id, contribution.id)] = 1
    print len(wordlists)


def prime_cache(args):
    """If data needs to be denormalized for lookup, do that here.
    This procedure should be separate from the db initialization, because
    it will have to be run periodiucally whenever data has been updated.
    """


if __name__ == '__main__':
    initializedb(create=main, prime_cache=prime_cache)
    sys.exit(0)
