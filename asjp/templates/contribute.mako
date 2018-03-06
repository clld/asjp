<%inherit file="home_comp.mako"/>
<%namespace name="util" file="util.mako"/>

<h3>Invitation to contribute</h3>
<p>
    Donations of data are welcome and we also invite more extended collaboration with
    interested parties.
    If you would like to contribute 40-item lists, please download these
    <a href="${request.static_url('asjp:static/Guidelines.pdf')}">brief guidelines</a>
    and use this <a href="${request.static_url('asjp:static/EnglishTemplate.doc')}">English
    template</a>
    or this <a href="${request.static_url('asjp:static/SpanishTemplate.doc')}">Spanish
    template</a>
    when filling in data (both are MS Word files).
</p>

<h4>Missing ISO 639-3 languages</h4>
<p>
    The following ${len(missing)} languages from Ethnologue 17 do not yet have wordlists
    in ASJP:
</p>
<div style="float: left">
        <%util:table items="${missing}" args="item" class_="table table-nonfluid table-striped">
    <%def name="head()">
        <th>ISO 639-3</th>
        <th>Ethnologue 17 name</th>
    </%def>
        <td>
            ${h.external_link("http://www-01.sil.org/iso639-3/documentation.asp?id=" + item[0], item[0])}
        </td>
        <td>
            ${h.external_link("http://www.ethnologue.com/language/" + item[0], item[1])}
        </td>
    </%util:table>
</div>
