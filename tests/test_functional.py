import pytest


@pytest.mark.parametrize(
    "method,path",
    [
        ('get_html', '/'),
        ('get_html', '/contribute'),
        ('get_html', '/software'),
        ('get', '/void.cldf.csv'),
        ('get_dt', '/parameters'),
        ('get_html', '/parameters'),
        ('get_html', '/parameters/1'),
        ('get_dt', '/contributions'),
        ('get_dt', '/languages?sSearch_3=gwj+gnk'),
        ('get_html', '/languages.map.html?sEcho=1&sSearch_3=gwj'),
        ('get_json', '/languages.geojson?sEcho=1&sSearch_3=gwj'),
        ('get', '/languages.txt?sEcho=1&sSearch_3=gwj'),
        ('get', '/languages/KICHEE_ALDEA_ARGUETA_SOLOLA.txt?sEcho=1&sSearch_3=gwj'),
        ('get_dt', '/values?language=KICHEE_ALDEA_ARGUETA_SOLOLA'),
        ('get_dt', '/values?parameter=1'),
        ('get_dt', '/sources'),
        ('get_html', '/sources/1'),
    ])
def test_pages(app, method, path):
    getattr(app, method)(path)
