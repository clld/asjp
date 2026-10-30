# Releasing the ASJP Database

Install clld app:
```shell
git clone --depth 1 https://github.com/clld/asjp
git clone --branch v21.1 --depth 1 https://github.com/lexibank/asjp asjp-cldf
curl -O https://iso639-3.sil.org/sites/iso639-3/files/downloads/iso-639-3_Code_Tables_20261015.zip
cd asjp
pip install -e .[test]
```
Recreate the database running
```
clld initdb development.ini --cldf ../asjp-cldf/cldf/cldf-metadata.json
```
Note: Computing the missing ISO codes requires a zip of the ISO 639-3 code tables.
Adapt the citation information on the download and the landing page.
Deploy to the production server.
Run the test suite:
```shell
pytest
```
Store the tested requirements:
```shell
pip freeze > requirements.txt
```
Store a db dump:
```shell
pg_dump -xO --compress gzip:9 asjp > asjp.sql.gz
```

