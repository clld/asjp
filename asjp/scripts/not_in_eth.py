from collections import OrderedDict

from csvw.dsv import reader
from clldutils.jsonlib import dump
from sqlalchemy import create_engine


eth17 = OrderedDict()
for l in reader('LanguageCodes.tab', dicts=True, delimiter='\t'):
    eth17[l['LangID']] = l['Name']

db = create_engine('postgresql://robert@/asjp')
in_asjp = set(r[0] for r in db.execute('select code_iso from doculect where code_iso is not null'))

missing = [(k, v) for k, v in eth17.items() if k not in in_asjp]
dump(missing, 'missing.json', indent=4)
