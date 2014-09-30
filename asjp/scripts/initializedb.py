# coding: utf8
from __future__ import unicode_literals, print_function
import sys
import codecs
import json
import re
from collections import defaultdict
import csv

import xlwt
from sqlalchemy import create_engine
from sqlalchemy.orm import joinedload_all
from unicsv import UnicodeCSVDictWriter
from clld.scripts.util import initializedb, Data, glottocodes_by_isocode
from clld.db.meta import DBSession
from clld.db.models import common
from clld.db.util import page_query
from clld.util import slug
from clld.lib.excel import hyperlink

import asjp
from asjp import models
from asjp.scripts.util import parse_sources


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


def source2wordlist(args, data, sources):
    revised = {}
    for d in csv.DictReader(open(args.data_file('unmatched_revised.csv'))):
        if d['match']:
            revised[(d['wiki'], d['name'])] = d['match']

    # slugs are unique except:
    # WEMBAWEMBA WEMBA_WEMBA wembawemba
    asjp_names = {}
    by_iso = defaultdict(list)
    for row in DBSession.query(models.Doculect.id, models.Doculect.code_iso):
        s = slug(row[0])
        if s in asjp_names:
            print(asjp_names[s], row[0], s)
        asjp_names[s] = row[0]
        if row[1]:
            by_iso[row[1]].append(row[0])

    matched = {}

    julia = 0
    names = 0
    iso = 0
    notes = 0
    missing = []
    for source in sources:
        sid = '%s-%s' % (source['href'], source['name'])

        if (source['href'].split('/')[-1], source['name']) in revised:
            julia += 1
            matched[sid] = revised[(source['href'].split('/')[-1], source['name'])]
            print(sid, matched[sid])
            continue

        if slug(source['name']) in asjp_names:
            names += 1
            matched[sid] = asjp_names[slug(source['name'])]
            continue
        if slug(source.get('asjp_name', 'aaaaaaaaaaaaaa')) in asjp_names:
            notes += 1
            matched[sid] = asjp_names[slug(source.get('asjp_name', 'aaaaaaaaaaaaaa'))]
            continue

        if ',' in source['name']:
            s = slug(' '.join(reversed(source['name'].split(','))))
            if s in asjp_names:
                names += 1
                matched[sid] = asjp_names[s]
                continue
        if '(' in source['name']:
            s = slug(' '.join(reversed(source['name'].split('('))))
            if s in asjp_names:
                names += 1
                matched[sid] = asjp_names[s]
                continue
        if 'dialect' in source['name']:
            s = slug(source['name'].replace('dialect', ''))
            if s in asjp_names:
                names += 1
                matched[sid] = asjp_names[s]
                continue
        if source.get('asjp_name'):
            s = slug(source['name'] + source['asjp_name']).replace('dialect', '')
            if s in asjp_names:
                names += 1
                matched[sid] = asjp_names[s]
                continue
        if source.get('iso') in by_iso:
            candidates = by_iso[source['iso']]
            if len(candidates) == 1:
                iso += 1
                matched[sid] = candidates[0]
                continue
            #print source['name'], '----', source.get('notes'), '-->', candidates
            missing.append((source, candidates))
            continue
        #print source['name'], '---iso:', source.get('iso'), '----', source.get('notes')
        missing.append((source, []))

    #
    # TODO: add candidates (determined by iso code) for un-matched entries!
    #
    print(names, 'from name')
    print(notes, 'from notes')
    print(iso, 'from iso')
    print(len(missing), 'missing')
    print(len(sources), '==', julia + names + notes + iso + len(missing))

    wb = xlwt.Workbook()
    ws = wb.add_sheet('Unmatched sources')

    fields = ['wiki', 'name', 'notes', 'iso', 'source', 'candidates', 'match']
    for i, col in enumerate(fields):
        ws.write(0, i, col)

    for j, item in enumerate(missing):
        source, candidates = item
        for i, col in enumerate(fields):
            if col in ['name', 'notes', 'iso', 'source']:
                value = source.get(col, '')
            elif col == 'wiki':
                value = hyperlink('https://lingweb.eva.mpg.de' + source['href'],
                                  source['href'].split('/')[-1])
            elif col == 'candidates' and candidates:
                value = ', '.join(candidates)
            else:
                value = ''
            ws.write(j + 1, i, value)

    with open(args.data_file('unmatched2.xls'), 'w') as fp:
        wb.save(fp)

    with open(args.data_file('matched.json'), 'w') as fp:
        json.dump(matched, fp)

    doculects_without_source = set(asjp_names.values()) - set(matched.values())
    print(len(doculects_without_source), 'without source')

    return matched


def add_codes(lang):
    for attr, prefix in dict(wals='wals_code_', iso='', glottolog='').items():
        code = getattr(lang, 'code_' + attr)
        if code:
            id_ = prefix + code
            identifier = common.Identifier.get(id_, default=None)
            if not identifier:
                identifier = common.Identifier(
                    id=id_,
                    name=code,
                    type=getattr(common.IdentifierType, attr).value)
            common.LanguageIdentifier(identifier=identifier, language=lang)


def main(args):
    glottocodes = glottocodes_by_isocode('postgresql://robert@/glottolog3')

    db = create_engine('postgresql://robert@/asjp')
    wordlists = {row[0]: 1 for row in db.execute('select id from language;')}

    sources = args.data_file('sources.json')
    if sources.exists():
        sources = json.load(open(sources))
    else:
        res = list(parse_sources(args))
        with open(sources, 'w') as fp:
            json.dump(res, fp)
        sources = res

    #-----
    with open(args.data_file('matched.json')) as fp:
        source2doculect = json.load(fp)

    nowordlist = 0
    with open(args.data_file('sources.csv'), 'w') as fp:
        writer = UnicodeCSVDictWriter(
            fp, 'href name author iso source notes wordlist'.split(), writeheader=True)

        for source in sorted(sources, key=lambda i: (i['href'], i['name'])):
            sid = '%s-%s' % (source['href'], source['name'])

            if source.get('author') and \
                    ('KE' in source['author']
                     or 'MP' in source['author']
                     or 'NA' in source['author']):
                print(source['author'], source2doculect.get(sid, '??'), source)

            if 'asjp_name' in source:
                del source['asjp_name']
            if not source['wordlist']:
                source['wordlist'] = source2doculect.get(sid, '')
            if source['wordlist'] not in wordlists:
                print('----->', source['wordlist'])
                nowordlist += 1
                source['wordlist'] = ''
            writer.writerow(source)

    # print nowordlist, 'sources missing a wordlist'
    # return
    # -----

    with codecs.open(args.data_file('listss16.txt'), encoding='latin1') as fp:
        wordlists = ['\n'.join(lines) for lines in parse(fp)]

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
        add_codes(lang)
        data.add(models.Doculect, lang.id, _obj=lang)

        if lang.code_iso:
            if lang.code_iso in langs_by_iso_code:
                langs_by_iso_code[lang.code_iso].append(lang)
            else:
                langs_by_iso_code[lang.code_iso] = [lang]

    #source2doculect = source2wordlist(args, data, sources)
    with open(args.data_file('matched.json')) as fp:
        source2doculect = json.load(fp)

    ls = {}
    cc = {}
    for i, source in enumerate(sources):
        contributors = []
        for contributor in re.split('\s*/\s*|,\s*|\s+and\s+', source.get('author', '')):
            contributor = contributor.strip()
            if contributor:
                if not contributor in data['Contributor']:
                    print('---missing---', contributor, '--source--', source)
                else:
                    contributors.append(data['Contributor'][contributor])
        if source['source'] in data['Source']:
            s = data['Source'][source['source']]
        else:
            s = data.add(common.Source, source['source'], id=str(i + 1), name=source['source'])

        sid = '%s-%s' % (source['href'], source['name'])
        if sid in source2doculect:
            if source2doculect[sid] not in data['Doculect']:
                print("unknown doculect ID in source2doculect", source2doculect[sid])
            else:
                lang = data['Doculect'][source2doculect[sid]]

        #langs = []
        #if source.get('asjp_name') in data['Doculect']:
        #    langs = [data['Doculect'][source['asjp_name']]]
        #elif source.get('iso') in langs_by_iso_code:
        #    langs = langs_by_iso_code[source['iso']]
        #elif source.get('name') and asjp_name(source.get('name', '')) in data['Doculect']:
        #    langs = [data['Doculect'][asjp_name(source['name'])]]
        #for lang in set(langs):
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
    print(len(wordlists))

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
    return
    q = DBSession.query(models.Doculect)\
        .order_by(models.Doculect.pk)\
        .options(
            joinedload_all(common.Language.valuesets, common.ValueSet.values),
            joinedload_all(common.Language.valuesets, common.ValueSet.parameter))
    previous = None
    for doculect in page_query(q, n=100, verbose=True, commit=True):
        doculect.txt = doculect.to_txt(previous=previous)
        previous = doculect

    #
    # TODO: include macroarea info from glottolog!
    #


if __name__ == '__main__':
    initializedb(create=main, prime_cache=prime_cache)
    sys.exit(0)
