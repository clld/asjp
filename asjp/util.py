from __future__ import print_function, unicode_literals
import re

from clld.db.meta import DBSession
from clld.db.models import common

from asjp import models


def normalize_classification(text, type=None):
    if not text:
        return ''
    new_nodes = []
    for i, node in enumerate(text.split('.' if type == 'wals' else ',')):
        if i == 0 and type == 'wals':
            new_nodes.append(node)
        else:
            new_nodes.append(' '.join(w.capitalize() for w in re.split('_|\-', node)))
    return ', '.join(new_nodes)


def dataset_detail_html(context=None, request=None, **kw):
    """
    #unique language names:  6895

    #Ethnologue families:  223

    #Glottolog families:  381

    #languages with unique ISO codes:  4424  match [a-z]{3}!

    asjp=# select count(*) from (select distinct name from identifier where type = 'iso639-3') as s;
-[ RECORD 1 ]
count | 4401

    #words in the database (not counting synonyms):  238976 and counting synonyms: ...
    """
    stats = {
        'wordlists': DBSession.query(common.Language.pk).count(),
        'ethnologue_families': DBSession.query(models.Doculect.ethnologue_family)
        .distinct().count(),
        'glottolog_families': DBSession.query(models.Doculect.glottolog_family)
        .distinct().count(),
        'iso_langs': DBSession.query(common.Identifier.name)
        .filter(common.Identifier.type == common.IdentifierType.iso.value).distinct()
        .count(),
        'synsets': DBSession.execute(
            'select count(*) from (select distinct valueset_pk from value) as s')
        .fetchone()[0],
        'words': DBSession.query(common.Value.pk).count(),
    }
    return stats
