import re
import pathlib

from clld.cliutil import Data, bibtex2source
from clld.db.meta import DBSession
from clld.db.models import common
from clld.lib.bibtex import Database
from pyasjp import ASJP
from pyasjp.models import Transcriber
from pyasjp.meanings import MEANINGS, MEANINGS_ALL

from asjp import models


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


def main(args):
    asjp = ASJP(args.cldf.tablegroup._fname.parent / '..' / 'raw')
    data = Data()

    dataset = common.Dataset(
        id='asjp',
        name="The ASJP Database",
        contact="wichmannsoeren@gmail.com",
        description="The Automated Similarity Judgment Program",
        domain='asjp.clld.org',
        publisher_name="Max Planck Institute for Evolutionary Anthropology",
        publisher_place="Leipzig",
        publisher_url="https://www.eva.mpg.de",
        license='https://creativecommons.org/licenses/by/4.0/',
        jsondata={
            'license_icon': 'cc-by.png',
            'license_name': 'Creative Commons Attribution 4.0 International License'})
    DBSession.add(dataset)

    editors = {'SW': 1, 'CB': 2, 'EH': 3}
    for spec in list(asjp.transcribers.values()) + [Transcriber('EH', 'Eric W. Holman')]:
        contributor = data.add(common.Contributor, spec.name, id=spec.id, name=spec.name)
        if spec.id in editors:
            DBSession.add(common.Editor(
                dataset=dataset,
                ord=editors[spec.id],
                contributor=contributor))

    for rec in Database.from_file(args.cldf.bibpath):
        data.add(common.Source, rec.id, _obj=bibtex2source(rec))

    cldf_params = {r['ID']: r for r in args.cldf['ParameterTable']}
    for id_ in sorted(MEANINGS_ALL.keys()):
        data.add(
            models.Meaning, id_,
            id=str(id_),
            name=MEANINGS_ALL[id_],
            core=id_ in MEANINGS,
            concepticon_id=cldf_params[str(id_)]['Concepticon_ID'],
            concepticon_gloss=cldf_params[str(id_)]['Concepticon_Gloss'],
        )

    cldf_langs = {r['Name']: r for r in args.cldf['LanguageTable']}
    cldf_sources = {}
    for row in args.cldf['FormTable']:
        cldf_sources[row['Language_ID']] = row['Source']

    for n, l in enumerate(asjp.iter_doculects()):
        cldf_lang = cldf_langs[l.id]

        lang = models.Doculect(
            id=l.id,
            name=l.name,
            latitude=l.latitude,
            longitude=l.longitude,
            code_wals=l.code_wals,
            code_iso=l.code_iso,
            code_glottolog=cldf_lang['Glottocode'],
            classification_ethnologue=l.classification_ethnologue,
            classification_glottolog=l.classification_glottolog,
            classification_wals=l.classification_wals,
            number_of_speakers=l.number_of_speakers,
            recently_extinct=l.recently_extinct,
            long_extinct=l.long_extinct,
            year_of_extinction=l.year_of_extinction,
            txt=str(l),
        )
        if l.classification_ethnologue:
            lang.ethnologue_family = l.classification_ethnologue.split(',')[0]

        if l.classification_glottolog:
            lang.glottolog_family = l.classification_glottolog.split(',')[0]

        if lang.classification_wals:
            family, genus = lang.classification_wals.split('.')
            lang.wals_family = family
            lang.wals_genus = genus
        add_codes(lang)

        lang = data.add(models.Doculect, lang.id, _obj=lang)
        contrib = data.add(common.Contribution, lang.id, id=lang.id, language=lang, name=lang.id)

        for synset in l.synsets:
            vsid = '%s-%s' % (lang.id, synset.meaning_id)
            vs = models.Synset(
                id=vsid,
                description=synset.comment,
                language=lang,
                contribution=contrib,
                parameter=data['Meaning'][synset.meaning_id])

            for i, word in enumerate(synset.words):
                models.Word(id='%s-%s' % (vsid, i + 1), name=word.form, valueset=vs, loan=word.loan)

        DBSession.flush()
        if cldf_lang['transcribers']:
            for i, transcriber in enumerate(cldf_lang['transcribers'].split(' and ')):
                common.ContributionContributor(
                    contribution=contrib,
                    contributor=data['Contributor'][transcriber],
                    ord=i + 1)

        for source in cldf_sources.get(l.id, []):
            DBSession.add(
                common.LanguageSource(language_pk=lang.pk, source_pk=data['Source'][source].pk))


def prime_cache(args):
    """If data needs to be denormalized for lookup, do that here.
    This procedure should be separate from the db initialization, because
    it will have to be run periodiucally whenever data has been updated.
    """
    from clldutils.iso_639_3 import ISO

    existing = set()
    for dl in DBSession.query(models.Doculect):
        if dl.code_iso:
            existing.add(dl.code_iso)

    iso = ISO(pathlib.Path(input('iso tables zipped: ')))
    for lang in iso.languages:
        if ('Sign Language' not in lang.name) and (lang.code not in existing):
            DBSession.add(common.Config(key='iso', value=lang.code, jsondata=dict(name=lang.name)))
