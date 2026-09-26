from pyramid.view import view_config

from clld.db.meta import DBSession
from clld.db.models import common
from clld.web.util.htmllib import HTML


@view_config(route_name='software', renderer='software.mako')
def software(req):
    def li(item):
        md = item.jsondata
        return HTML.li(f'{md["Author"]}. {md["Year"]}. ', HTML.a(f'{md["Description"]}.', href=md['s3url']))

    files = [
        li(cfg) for cfg in
        DBSession.query(common.Config).filter(common.Config.value.in_([
            'AlgorithmTreeFromLabels.zip',
            'DistanceCorrelationsProgram.zip',
            'NewickReader.zip',
            'ASJPSoftware003.zip',
            'ASJPdates-02.zip',
            'asjp79a.zip',
            'mega_nexus.zip',
            'geo_dist.zip',
            'string_distances.py',
        ]))]
    return {'files': files}


@view_config(route_name='contribute', renderer='contribute.mako')
def contribute(req):
    return {
        'files': {
            cfg.value: cfg.jsondata['s3url'] for cfg in
            DBSession.query(common.Config).filter(common.Config.value.in_([
                'Guidelines.pdf',
                'EnglishTemplate.doc',
                'SpanishTemplate.doc',
            ]))
        },
        'missing': [
            (i.value, i.jsondata['name']) for i in
            DBSession.query(common.Config)
            .filter(common.Config.key == 'iso')
            .order_by(common.Config.value)]}
