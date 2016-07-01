from pyramid.view import view_config
from clldutils.path import Path

from clldutils.jsonlib import load

import asjp


@view_config(route_name='software', renderer='software.mako')
def software(req):
    return {}


@view_config(route_name='contribute', renderer='contribute.mako')
def contribute(req):
    return {'missing': load(
        Path(asjp.__file__).parent.joinpath(
            'static', 'ethnologue17_diff.json'))['missing']}
