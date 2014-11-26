from sqlalchemy import not_

from clld.util import jsonload
from clld.scripts.util import parsed_args
from clld.db.meta import DBSession
from clld.db.models.common import LanguageSource
from clld.lib.dsv import reader, UnicodeWriter

from asjp.models import Doculect


def main(args):
    sources = jsonload(args.data_file('sources.json'))
    fields = ['href', 'name', 'author', 'iso', 'source', 'notes', 'wordlist']
    with UnicodeWriter(args.data_file('..', 'sources.csv')) as fp:
        fp.writerow(fields)
        for source in sorted(sources, key=lambda i: i['name']):
            fp.writerow([source.get(f, '') for f in fields])
    return
    ethnologue_names = {
        r.ISO_639: r.Language_Name for r in reader(args.data_file(
        '..', '..', 'ethnologue-17-data', 'Table_of_Languages.tab'), namedtuples=True)}

    # ASJP name for language, Ethnologue's name, ISO code
    rows = [['ASJP Name', 'Ethnologue name', 'ISO code']]
    subquery = DBSession.query(LanguageSource.language_pk).distinct().subquery()
    for i, l in enumerate(DBSession.query(Doculect).order_by(Doculect.pk).filter(not_(Doculect.pk.in_(subquery)))):
        rows.append([l.id, ethnologue_names.get(l.code_iso, ''), l.code_iso or ''])
    #print i
    with UnicodeWriter(args.data_file('..', 'doculects_without_source.csv')) as fp:
        fp.writerows(rows)


if __name__ == '__main__':
    main(parsed_args())
