from pyramid.view import view_config


@view_config(route_name='software', renderer='software.mako')
def software(req):
    return {}
