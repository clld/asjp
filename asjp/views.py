from pyramid.view import view_config

from asjp.util import missing_iso


@view_config(route_name='software', renderer='software.mako')
def software(req):
    return {}


@view_config(route_name='contribute', renderer='contribute.mako')
def contribute(req):
    return {'missing': missing_iso()}
