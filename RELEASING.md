# Releasing the ASJP Database

Releases of the ASJP Database are curated in https://github.com/lexibank/asjp
Once the lexibank repo is released, the data can be loaded into the web app.

- Recreate the database running
  ```
  clld initdb development.ini --glottoog ... --cldf ...
  ```
- Adapt the citation information on the download and the landing page.
- Deploy to the production server.
