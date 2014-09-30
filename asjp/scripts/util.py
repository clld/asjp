# coding: utf8
from __future__ import unicode_literals
import re

import requests
from bs4 import BeautifulSoup as bs

from clld.util import slug


def get(args, path):
    fpath = args.data_file('sources', path.split('/')[-1] + '.html')
    if not fpath.exists():
        content = requests.get(
                "https://lingweb.eva.mpg.de" + path, verify=False).content
        with open(fpath, 'w') as fp:
            fp.write(content)
    else:
        with open(fpath) as fp:
            content = fp.read()
    return bs(content)


def asjp_name(name):
    if '"' in name:
        name = name.split('"')[1]
    name = name.replace("'", "").replace(" ", "_").replace("/", "_").upper()
    name = '_'.join(slug(p) for p in name.split('_'))
    if name.startswith('proto') and not name.startswith('proto_'):
        name = name.replace('proto', 'proto_', 1)
    return name.upper()


def text(n):
    return ' '.join(list(n.stripped_strings))


def parse_sources(args):
    """
    https://lingweb.eva.mpg.de/asjp/index.php/ASJP
    <ul><li> <a href="/asjp/index.php/A1"

    https://lingweb.eva.mpg.de//asjp/index.php/A1
<table border="1">

<tr>
<th> Name
</th><th> SIL
</th><th> Author
</th><th> Source
</th><th> Notes
</th></tr>
<tr>
<td> <a href="/asjp/index.php?title=A-Pucikwar_language&amp;action=edit&amp;redlink=1"
class="new" title="A-Pucikwar language (page does not exist)"
      >A-Pucikwar</a>
</td>
<td> apq </td>
<td> AKW </td>
<td> Man, Edward Horace. 1919-1923. Dictionary of the South Andaman language. Bombay:
Education Society Press. </td>
<td> = "South Andaman"</td>
</tr>
    """
    fields = 'name iso author source notes'.split()

    ul = get(args, '/asjp/index.php/ASJP').find('ul')
    for a in ul.find_all('a'):
        table = get(args, a['href']).find('table')
        for tr in table.find_all('tr'):
            source = {'href': a['href']}
            for i, td in enumerate(tr.find_all('td')):
                t = text(td)
                if t:
                    if i < len(fields):
                        source[fields[i]] = t
                    #else:
                    #    print t
                    #    print tr
            if source.get('notes'):
                source['asjp_name'] = asjp_name(source['notes'])
            if re.match('[a-z]{3}$', source.get('author', '')) and source.get('iso'):
                # switch author and iso code in case they have obviously been confused.
                source['author'], source['iso'] = source['iso'], source['author']
            if source and source.get('source'):
                source['wordlist'] = ''
                if '=' in source.get('notes', ''):
                    l = source['notes'].split('=')[1].replace('"', '').strip()
                    source['wordlist'] = asjp_name(l)
                elif source.get('name'):
                    source['wordlist'] = asjp_name(source['name'])
                yield source
