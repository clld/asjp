from clld.web.assets import environment
from path import path

import asjp


environment.append_path(
    path(asjp.__file__).dirname().joinpath('static'), url='/asjp:static/')
environment.load_path = list(reversed(environment.load_path))
