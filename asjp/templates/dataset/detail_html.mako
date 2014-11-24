<%inherit file="../home_comp.mako"/>

<div class="row-fluid">
<h2>${request.dataset.description}</h2>
</div>

<div class="row-fluid">
    <div class="span4 well well-small">
        <h3>How to cite:</h3>
        <p>
            Wichmann, Søren, André Müller, Annkathrin Wett, Viveka Velupillai, Julia Bischoffberger, Cecil H. Brown, Eric W. Holman, Sebastian Sauppe, Zarina Molochieva, Pamela Brown, Harald Hammarström, Oleg Belyaev, Johann-Mattis List, Dik Bakker, Dmitry Egorov, Matthias Urban, Robert Mailhammer, Agustina Carrizo, Matthew S. Dryer, Evgenia Korovina, David Beck, Helen Geyer, Pattie Epps, Anthony Grant, and Pilar Valenzuela. 2013. The ASJP Database (version 16).
        </p>
    </div>
    <div class="span4" style="padding: 20px; text-align: center;">
        <img width="200" height="200" src="${request.static_url('asjp:static/logo_asjp.gif')}" class="image"/>
    </div>
    <div class="span4">

        <table class="table table-nonfluid">
            <tbody>
            <tr>
                <th>
                    <a href="${request.route_url('languages')}">Wordlists</a>
                </th><td class="right">${wordlists}</td>
            </tr>
            <tr>
                <th>Synsets</th><td class="right">${synsets}</td>
            </tr>
            <tr>
                <th>Words</th><td class="right">${words}</td>
            </tr>
            <tr>
                <th>Distinct ISO 639-3 languages</th><td class="right">${iso_langs}</td>
            </tr>
            <tr>
                <th>
                    <a href="${request.route_url('contribute')}">
                        Missing ISO 639-3 languages (from Ethnologue 17)
                    </a>
                </th>
                <td class="right">3156</td>
            </tr>
            <tr>
                <th>Ethnologue families</th><td class="right">${ethnologue_families}</td>
            </tr>
            <tr>
                <th>
                    ${h.external_link('http://glottolog.org/glottolog/family', label='Glottolog families')}
                </th>
                <td class="right">${glottolog_families}</td>
            </tr>
            </tbody>
        </table>
    </div>

</div>
