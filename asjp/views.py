import json

from pyramid.view import view_config
from path import path

from clld.util import jsonload

import asjp


@view_config(route_name='software', renderer='software.mako')
def software(req):
    return {}


@view_config(route_name='contribute', renderer='contribute.mako')
def contribute(req):
    return {'missing': jsonload(
        path(asjp.__file__).dirname().joinpath(
            'static', 'ethnologue17_diff.json'))['missing']}
