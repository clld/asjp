from functools import partial

from clld.web.app import get_configurator, menu_item
from clld import interfaces

# we must make sure custom models are known at database initialization!
from asjp import models


_ = lambda s: s
_('Contribution')
_('Contributions')
_('Parameter')
_('Parameters')


def link_attrs(req, obj, **kw):
    if interfaces.IContribution.providedBy(obj):
        kw['href'] = req.route_url('language', id=obj.id, **kw.pop('url_kw', {}))
    return kw


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    utilities = [
        (link_attrs, interfaces.ILinkAttrs),
    ]
    config = get_configurator('asjp', *utilities, **dict(settings=settings))
    config.include('clldmpg')
    config.register_menu(
        ('dataset', partial(menu_item, 'dataset', label='Home')),
        ('languages', partial(menu_item, 'languages')),
        ('parameters', partial(menu_item, 'parameters')),
        ('sources', partial(menu_item, 'sources')),
    )
    return config.make_wsgi_app()
