from functools import partial

from clld.web.app import get_configurator, menu_item

# we must make sure custom models are known at database initialization!
from asjp import models


_ = lambda s: s
_('Contribution')
_('Contributions')
_('Parameter')
_('Parameters')


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = get_configurator('asjp', settings=settings)
    config.register_menu(
        ('dataset', partial(menu_item, 'dataset', label='Home')),
        ('languages', partial(menu_item, 'languages')),
        ('contributions', partial(menu_item, 'contributions')),
        ('parameters', partial(menu_item, 'parameters')),
        ('sources', partial(menu_item, 'sources')),
    )
    config.include('asjp.datatables')
    config.include('asjp.adapters')
    config.include('asjp.maps')
    return config.make_wsgi_app()
