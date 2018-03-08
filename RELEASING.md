# Releasing the ASJP Database

The ASJP Database is updated infrequently (see http://asjp.clld.org/download).
Data for a new release comes in two files,
- the wordlists in the ASJP format, in a file `listss<version>.txt`
- the sources in an excel spreadsheet `sources_listss<version>.xlsx`

Additionally, a mapping from initials to full names of contributors is
provided in https://github.com/clld/asjp-data/blob/master/initials_transcribers.txt

A new release is now done as follows:

1. Upload the two new files to `clld/asjp-data`
2. Adapt the filenames in `asjp/scripts/initializedb.py` and `asjp/scripts/util.py`
3. Recreate the database running `python asjp/scripts/initializedb.py development.ini`
4. Recreate the list of missing Ethnologue 17 languages (`asjp/static/ethnologue17_diff.json`) running `asjp/scripts/not_in_eth.py`  FIXME: this script needs to be adapted to spit out the file at the correct location!
5. Add a zipped version of `listss<version>.txt` to `asjp/static` and link to it from the download page `asjp/templates/download.mako`.
6. Adapt the citation information in `asjp/templates/dataset/detail_html.mako`
7. Release this repository to trigger archiving with ZENODO.
8. Release `clld/asjp-data` to trigger archiving with ZENODO.
9. Create downloads running `clld-create-downloads development.ini`.
10. Upload downloads to cdstar running `clldmpg --version=<version> dl2cdstar`.
11. Commit and push the updated cdstar catalogs.
12. Deploy to the production server.
