# coding: utf8
from __future__ import unicode_literals, print_function
import re

import xlrd


YEAR_PATTERN = re.compile('(\s+|^)\(?(?P<year>[12][0-9]{3}(\-[0-9]{2})?)\)?\.?\s*')


def pc_with(s):
    if s .endswith(', personal communication.') or s.endswith(', p.c.'):
        return ','.join(s.split(',')[:-1]).strip()
    if s.endswith(' (personal communication).'):
        return s[:-len(' (personal communication).')]


def get_year(s):
    if isinstance(s, float):
        return '%s' % int(s)
    s = s.strip() or None
    if s == 'n.d.':
        return None
    return s


def clean_title(s):
    s = s.strip()
    if s.startswith('['):
        if s.endswith(']'):
            s = s[1:-1].strip()
        elif s.endswith('].'):
            s = s[1:-2].strip()
    return s


def itersources(row):
    author = row['AUTHOR'].strip() or None
    year = get_year(row['YEAR'])

    for i, chunk in enumerate(clean_title(row['TITLE_ETC']).split(';')):
        chunk = clean_title(chunk)
        if i == 0:
            if author or year or chunk:
                yield author, year, chunk
        else:
            match = YEAR_PATTERN.search(chunk)
            if match:
                yield (
                    chunk[:match.start()].strip() or None,
                    match.group('year'),
                    chunk[match.end():].strip())
            else:
                pc = pc_with(chunk)
                if pc:
                    yield pc, None, 'personal communication'
                else:
                    yield None, None, chunk


class Meta(object):
    def __init__(self, row, transcriber_map):
        self.transcribers = []
        for initial in row['LIST_MADE_BY'].split('/'):
            initial = initial.strip()
            if initial:
                if initial == 'Matthias Pache':
                    initial = 'MP'
                if initial == 'MDS':
                    initial = 'MSD'
                if initial == 'TVV -> AM':
                    initial = 'AM'
                if initial == 'SP':
                    initial = 'PS'
                if initial not in transcriber_map:
                    raise ValueError(initial)
                self.transcribers.append(initial)

        self.sources = list(itersources(row))


def get_transcriber_map(args):
    transcriber_map = {}
    for line in args.data_file('initials_transcribers.txt').open(encoding='latin1'):
        initial, name = [s.strip() for s in line.split('\t')]
        transcriber_map[initial] = name
    return transcriber_map


def parse_meta(args):
    transcriber_map = get_transcriber_map(args)
    sources = {}
    wb = xlrd.open_workbook(args.data_file('sources_listss18.xlsx').as_posix())
    sheet = wb.sheet_by_name('SourcesListss17')
    for i in range(sheet.nrows):
        row = [col.value for col in sheet.row(i)]
        if i == 0:
            cols = row
        else:
            row = dict(zip(cols, row))
            if row['ASJP_NAME'].strip():
                sources[row['ASJP_NAME'].strip()] = Meta(row, transcriber_map)
    return sources

"""
--- TONGA_AFRICA
--- SHIRA_YUGUR
--- TEWA_SAN_JUAN_PUEBLO

--- BWETAWIT
--- EJA
--- EMILIANO_REGGIANO
--- ROMAGNOL_REVENNATE
--- PROTO_SOUTH_SOUTH_SULAWESI
--- CHINANTEC_TEPETOTULA


WETAWIT
ROMAGNOL_RAVENNATE
CHINANTEC_TEPETOTUTLA
EMILANO_REGGIANO
PROTO_SOUTH_SULAWESI
BEJA

SONAI_YAEYAMA

istss17:

--- BWETAWIT

change to WETAWIT

--- EJA

change to BEJA

--- EMILIANO_REGGIANO

no action

--- ROMAGNOL_REVENNATE

change to ROMAGNOL_RAVENNATE

--- PROTO_SOUTH_SOUTH_SULAWESI

change to PROTO_SOUTH_SULAWESI

--- CHINANTEC_TEPETOTULA

change to CHINANTEC_TEPETOTUTLA

excel:

WETAWIT

no action

ROMAGNOL_RAVENNATE

no action

CHINANTEC_TEPETOTUTLA

no action

EMILANO_REGGIANO

change to EMILIANO_RAGGIANO

PROTO_SOUTH_SULAWESI

no action

BEJA

no action

This leaves us with three wordlists in listss17 with no row in the excel sheet:

TONGA_AFRICA

rename this TONGA in listss17. In the excel sheet there are two almost identical entries for TONGA. Delete the one that lacks a dot after "etc" in the title.

SHIRA_YUGUR

make a row in the excel sheet with just the name and no information on sources etc.

TEWA_SAN_JUAN_PUEBLO

make a row in the excel sheet with just the name and no information on sources etc.


And one row in the excel sheet which doesn't match a wordlist:

SONAI_YAEYAMA

Delete this row in the excel sheet.
"""
