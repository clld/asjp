# coding: utf8
from __future__ import unicode_literals

from sqlalchemy import create_engine
from sqlalchemy.orm import create_session
from clld.db.meta import Base


def test_asjp_name():
    from asjp.models import asjp_name

    assert asjp_name('"name"') == 'NAME'
    assert asjp_name("'name") == 'NAME'
    assert asjp_name('"na me"') == 'NA_ME'
    assert asjp_name('"na/me"') == 'NA_ME'


def test_doculect():
    from asjp.models import Doculect, Meaning

    engine = create_engine('sqlite://')
    Base.metadata.create_all(engine)
    session = create_session(engine)
    session.add(Meaning(id='1', name='I'))
    session.flush()
    d = Doculect.from_txt("""\
KICHEE_ALDEA_ARGUETA_SOLOLA{May.MAYAN|Mayan,Yucatecan-CoreMayan,K'ichean-Mamean,K'ichean,Poqom-K'ichean,CoreK'ichean@Mayan,Yucatecan-CoreMayan,CoreMayan,Quichean-Mamean,GreaterQuichean,Poqom-Quichean,CoreQuichean,Quiche-Achi}
 1   14.78  -91.50     2330000   qch   quc
1. I	in, %other //
""", session=session)
    d.to_txt()
    d.long_extinct = True
    d.to_txt()
    d.recently_extinct = True
    d.to_txt()
    d.year_of_extinction = 1800
    d.to_txt()
    assert d.id == 'KICHEE_ALDEA_ARGUETA_SOLOLA'
    d.wals_genus = 'x'
    d.wals_family = 'x'
    assert d.href('wals_genus')
    assert d.href('wals_family')
    assert d.href('wals')
    assert d.format_words(None) == ''


def test_normalize_classification():
    from asjp.util import normalize_classification

    assert normalize_classification(None) == ''
