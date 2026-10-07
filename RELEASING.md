# Releasing the ASJP Database

Releases of the ASJP Database are curated in https://github.com/lexibank/asjp
Once the lexibank repo is released, the data can be loaded into the web app.

- Install clld app:
  ```shell
  git clone --depth 1 https://github.com/clld/asjp
  cd asjp
  pip install -e .[test]
  ```
- Recreate the database running
  ```
  clld initdb development.ini --glottolog ../../glottolog/glottolog --cldf ../../asjp/asjp-cldf/cldf/cldf-metadata.json
  ```
  Note: Computing the missing ISO codes requires a zip of the ISO 639-3 code tables.
- Adapt the citation information on the download and the landing page.
- Deploy to the production server.
- Run the test suite:
  ```shell
  pytest
  ```
- Store the tested requirements:
  ```shell
  pip freeze > requirements.txt
  ```
- Store a db dump:
  ```shell
  pg_dump -xO asjp > asjp.sql
  zip asjp.sql.zip asjp.sql
  rm asjp.sql
  ```

