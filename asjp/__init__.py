from pyramid.config import Configurator

from clld import interfaces
from clld.web.adapters.cldf import CldfConfig
from clld.db.models.common import Value

# we must make sure custom models are known at database initialization!
from asjp import models


_ = lambda s: s
_('Language')
_('Languages')
_('Contribution')
_('Contributions')
_('Parameter')
_('Parameters')


class ASJPCldfConfig(CldfConfig):
    def custom_schema(self, req, ds):
        ds.add_columns('FormTable', {'name': 'Loan', 'datatype': 'boolean'})

    def convert(self, model, item, req):
        res = CldfConfig.convert(self, model, item, req)
        if model == Value:
            res['Loan'] = item.loan
            res['Source'] = [s.id for s in item.valueset.language.sources]
        return res


def link_attrs(req, obj, **kw):
    if interfaces.IContribution.providedBy(obj):
        kw['href'] = req.route_url('language', id=obj.id, **kw.pop('url_kw', {}))
    return kw


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include('clldmpg')
    config.registry.registerUtility(link_attrs, interfaces.ILinkAttrs)
    config.registry.registerUtility(ASJPCldfConfig(), interfaces.ICldfConfig)
    home_comp = config.registry.settings['home_comp']
    home_comp.append('software')
    home_comp.append('contribute')
    config.add_settings(home_comp=home_comp)
    config.add_route('software', '/software')
    config.add_route('contribute', '/contribute')
    return config.make_wsgi_app()
