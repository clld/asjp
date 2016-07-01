from clld.web.assets import environment
from clldutils.path import Path

import asjp


environment.append_path(
    Path(asjp.__file__).parent.joinpath('static').as_posix(), url='/asjp:static/')
environment.load_path = list(reversed(environment.load_path))
