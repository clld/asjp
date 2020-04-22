import pathlib

from clld.web.assets import environment

import asjp


environment.append_path(
    str(pathlib.Path(asjp.__file__).parent.joinpath('static')), url='/asjp:static/')
environment.load_path = list(reversed(environment.load_path))
