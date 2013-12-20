from clld.tests.util import TestWithSelenium

import asjp


class Tests(TestWithSelenium):
    app = asjp.main({}, **{'sqlalchemy.url': 'postgres://robert@/asjp'})
