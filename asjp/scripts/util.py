# coding: utf8
from __future__ import unicode_literals
import re
import codecs

import requests
from bs4 import BeautifulSoup as bs


MEANINGS = {
    1: 'I',
    2: 'you',
    3: 'we',
    11: 'one',
    12: 'two',
    18: 'person',
    19: 'fish',
    21: 'dog',
    22: 'louse',
    23: 'tree',
    25: 'leaf',
    28: 'skin',
    30: 'blood',
    31: 'bone',
    34: 'horn',
    39: 'ear',
    40: 'eye',
    41: 'nose',
    43: 'tooth',
    44: 'tongue',
    47: 'knee',
    48: 'hand',
    51: 'breast',
    53: 'liver',
    54: 'drink',
    57: 'see',
    58: 'hear',
    61: 'die',
    66: 'come',
    72: 'sun',
    74: 'star',
    75: 'water',
    77: 'stone',
    82: 'fire',
    85: 'path',
    86: 'mountain',
    92: 'night',
    95: 'full',
    96: 'new',
    100: 'name',
}

WORD_LINE_PATTERN = re.compile('|'.join('%s\s+\w+\t' % k for k in MEANINGS))
LANGUAGE_LINE_PATTERN = re.compile('(?P<name>[^\{]+)\{(?P<wals>[^\|]*)\|(?P<ethnologue>[^\@]*)\@(?P<glottolog>[^\}]*)\}?')


def parse_metadata(line):
    """
    The second line gives properties of the languages, in fixed format separated by blanks (not tabs),
    so the columns are important.

    Col. 2: 3 if the language is the first one in a new WALS family, 2 if it’s the first
    language in a new WALS genus, 1 otherwise.

    Col. 4-10, right justified: latitude in degrees and
    hundredths of a degree; minus means South.

    Col. 12-18, right justified: longitude in degrees a
    nd hundredths of a degree; minus means West.
    Latitudes and longitudes were ascertained from WALS, or from the maps in Ethnologue or
    Moseley and Asher (1994), or from information in the source for the list.

    Col. 19-30, right justified: number of speakers, from Ethnologue. This number always
    refers to the entire language, as defined in Ethnologue, even if the list itself
    refers to a dialect. The number is

        0 if the number of speakers is unknown;
        -1 if the language is recently extinct;
        -2 if the language is long extinct;
        or if the approximate date of extinction is known, the date is preceded by a minus sign.

    In the ASJP software, if there is a date in the first line of the entire file, lists
    with earlier extinction dates here are ignored, as are lists with -2; otherwise, all
    lists are read.

    Col. 34-36: three-letter WALS code, if any.

    Col. 40-42: three-letter ISO639-3 code, if any. This code is included for languages in
    previous editions of Ethnologue even if they aren’t in the 17th edition. Languages
    that lack an ISO639-3 code but can be placed in the Ethnologue classification are given
    a code consisting of two letters followed by the number 0 (for use in ASJP software).
    """
    lat = line[4:11].strip()
    lng = line[11:18].strip()
    nos = int(line[18:30].strip() or 0)
    return dict(
        latitude=float(lat) if lat else None,
        longitude=float(lng) if lng else None,
        number_of_speakers=nos if nos >= 0 else 0,
        extinct=nos < 0,
        year_of_extinction=abs(nos) if nos < -2 else None,
        wals=line[33:36].strip() or None,
        iso=line[39:42].strip() or None)


def parse_word(line):
    header, body = line.split('\t', 1)
    body = body.strip()
    comment = None
    if re.search('  | //', body):
        body, comment = re.split('  | //', body, 1)
    words = []
    for word in body.split(','):
        word = word.strip()
        if word != 'XXX':
            if word.startswith('%'):
                words.append((word[1:], True))
            else:
                words.append((word, False))
    return int(header.split()[0]), words, comment or None


def parse(fp):
    language = None
    in_header = False

    for line in fp:
        if in_header:
            # parse the second line of language metadata:
            language.update(parse_metadata(line))
            in_header = False
            continue
        m = LANGUAGE_LINE_PATTERN.match(line)
        if m:
            if language:
                yield language
            language = m.groupdict()
            language['words'] = {}
            in_header = True
        m = WORD_LINE_PATTERN.match(line)
        if m:
            index, words, comment = parse_word(line)
            language['words'][index] = words, comment

    if language:
        yield language


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
    return name.replace("'", "").replace(" ", "_").replace("/", "_").upper()


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
<td> <a href="/asjp/index.php?title=A-Pucikwar_language&amp;action=edit&amp;redlink=1" class="new" title="A-Pucikwar language (page does not exist)"
      >A-Pucikwar</a>
</td>
<td> apq </td>
<td> AKW </td>
<td> Man, Edward Horace. 1919-1923. Dictionary of the South Andaman language. Bombay: Education Society Press. </td>
<td> = "South Andaman"</td>
</tr>
    """
    fields = 'name iso author source notes'.split()

    ul = get(args, '/asjp/index.php/ASJP').find('ul')
    for a in ul.find_all('a'):
        table = get(args, a['href']).find('table')
        for tr in table.find_all('tr'):
            source = {}
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
                source['author'], source['iso'] = source['iso'], source['author']
            if source and source.get('source'):
                yield source
