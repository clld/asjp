# coding: utf8
from __future__ import unicode_literals
import sys
import codecs
import json
import re

import transaction
from sqlalchemy import create_engine
from sqlalchemy.orm import joinedload_all
from clld.scripts.util import initializedb, Data
from clld.db.meta import DBSession
from clld.db.models import common
from clld.db.util import page_query

import asjp
from asjp import models
from asjp.scripts.util import parse_sources, asjp_name


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


GC = create_engine('postgresql://robert@/glottolog3')

#
# TODO: include macroarea info from glottolog!
#
glottocodes = {}
for row in GC.execute('select ll.hid, l.id from language as l, languoid as ll where ll.pk = l.pk'):
    if row[0] and len(row[0]) == 3:
        glottocodes[row[0]] = row[1]


def main(args):
    with codecs.open(args.data_file('listss16.txt'), encoding='latin1') as fp:
        wordlists = ['\n'.join(lines) for lines in parse(fp)]

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

    for id_ in sorted(models.MEANINGS_ALL.keys()):
        data.add(
            models.Meaning, id_,
            id=str(id_), name=models.MEANINGS_ALL[id_], core=id_ in models.MEANINGS)

    # keep a mapping of iso codes to wordlists to associate sources lateron
    langs_by_iso_code = {}
    for l in wordlists:
        lang = models.Doculect.from_txt(l)
        lang.code_glottolog = glottocodes.get(lang.code_iso)
        lang.add_codes()
        data.add(models.Doculect, lang.id, _obj=lang)

        if lang.code_iso:
            if lang.code_iso in langs_by_iso_code:
                langs_by_iso_code[lang.code_iso].append(lang)
            else:
                langs_by_iso_code[lang.code_iso] = [lang]

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
        if source.get('asjp_name') in data['Doculect']:
            langs = [data['Doculect'][source['asjp_name']]]
        elif source.get('iso') in langs_by_iso_code:
            langs = langs_by_iso_code[source['iso']]
        elif source.get('name') and asjp_name(source.get('name', '')) in data['Doculect']:
            langs = [data['Doculect'][asjp_name(source['name'])]]
        for lang in set(langs):
            if (lang.id, s.id) not in ls:
                lang.sources.append(s)
                ls[(lang.id, s.id)] = 1
            contribution = lang.wordlist
            for contributor in set(contributors):
                if (contributor.id, contribution.id) not in cc:
                    DBSession.add(common.ContributionContributor(
                        contribution=contribution,
                        contributor=contributor))
                    cc[(contributor.id, contribution.id)] = 1
    print len(wordlists)

    #print models.txt_header()
    #previous = None
    #for doculect in DBSession.query(models.Doculect).order_by(models.Doculect.pk).limit(3):
    #    print doculect.to_txt(previous=previous)
    #    previous = doculect


def prime_cache(args):
    """If data needs to be denormalized for lookup, do that here.
    This procedure should be separate from the db initialization, because
    it will have to be run periodiucally whenever data has been updated.
    """
    q = DBSession.query(models.Doculect)\
        .order_by(models.Doculect.pk)\
        .options(
            joinedload_all(common.Language.valuesets, common.ValueSet.values),
            joinedload_all(common.Language.valuesets, common.ValueSet.parameter))
    previous = None
    for doculect in page_query(q, n=100, verbose=True, commit=True):
        doculect.txt = doculect.to_txt(previous=previous)
        previous = doculect


if __name__ == '__main__':
    initializedb(create=main, prime_cache=prime_cache)
    sys.exit(0)
