# Releasing the ASJP Database

Releases of the ASJP Database are curated in https://github.com/lexibank/asjp
Once the lexibank repo is released, the data can be loaded into the web app.

- Recreate the database running
  ```
  clld initdb development.ini --glottoog ... --cldf ...
  ```
  Note: Computing the missing ISO codes requires a zip of the ISO 639-3 code tables.
- Adapt the citation information on the download and the landing page.
- Deploy to the production server.
