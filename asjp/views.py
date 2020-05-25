from pyramid.view import view_config

from clld.db.meta import DBSession
from clld.db.models import common


@view_config(route_name='software', renderer='software.mako')
def software(req):
    return {}


@view_config(route_name='contribute', renderer='contribute.mako')
def contribute(req):
    return {
        'missing': [
            (i.value, i.jsondata['name']) for i in
            DBSession.query(common.Config)
            .filter(common.Config.key == 'iso')
            .order_by(common.Config.value)]}
