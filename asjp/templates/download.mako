<%inherit file="home_comp.mako"/>

<h3>Downloads</h3>

<div class="row-fluid">
<div class="span5 well well-small">
    <dl>
    % for model, dls in h.get_downloads(request):
        <dt>${_(model)}</dt>
        % for dl in dls:
        <dd>
            <a href="${dl.url(request)}">${dl.label(req)}</a>
        </dd>
        % endfor
    % endfor
    </dl>
</div>
<div class="span6">
    <p>
        Downloads are provided as
        ${h.external_link("http://en.wikipedia.org/wiki/Zip_%28file_format%29", label="zip archives")}
        bundling the data and a
        ${h.external_link("http://en.wikipedia.org/wiki/README", label="README")}
        file.
    </p>
</div>
</div>
<div class="row-fluid">
    <h4>Earlier versions of the ASJP World Language Tree of lexical similarity</h4>
    <table class="table">
        <thead>
            <tr><th>Version no.</th><th>Cite as</th></tr>
        </thead>
        <tbody>
        <tr>
            <td>
                <a href="${request.static_url('asjp:static/WorldLanguageTree-001.pdf')}">001 [PDF]</a>
            </td>
            <td>
                André Müller, Viveka Velupillai, Søren Wichmann, Cecil H. Brown, Pamela Brown, Eric W. Holman, Dik Bakker, Oleg Belyaev, Dmitri Egorov, Robert Mailhammer, Anthony Grant, and Kofi Yakpo. 2009. ASJP World Language Tree: Version 1 (April 2009).
            </td>
        </tr>
        <tr>
            <td>
                <a href="${request.static_url('asjp:static/WorldLanguageTree-002.pdf')}">002 [PDF]</a>
            </td>
            <td>
                André Müller, Viveka Velupillai, Søren Wichmann, Cecil H. Brown, Pamela Brown, Eric W. Holman, Dik Bakker, Oleg Belyaev, Dmitri Egorov, Robert Mailhammer, Anthony Grant, and Kofi Yakpo. 2009. ASJP World Language Tree of Lexical Similarity: Version 2 (April 2009).
            </td>
        </tr>
            <tr>
                <td>
                    <a href="${request.static_url('asjp:static/WorldLanguageTree-003.pdf')}">003 [PDF]</a>
                </td>
                <td>
                    Müller, André, Søren Wichmann, Viveka Velupillai, Cecil H. Brown, Pamela Brown, Sebastian Sauppe, Eric W. Holman, Dik Bakker, Johann-Mattis List, Dmitri Egorov, Oleg Belyaev, Robert Mailhammer, Matthias Urban, Helen Geyer, and Anthony Grant. 2010. ASJP World Language Tree of Lexical Similarity: Version 3 (July 2010).
                </td>
            </tr>
        </tbody>
    </table>
    <h4>Earlier versions of the ASJP Database</h4>
    <table class="table table-nonfluid">
        <thead>
        <tr><th>Version no.</th><th>Cite as</th></tr>
        </thead>
        <tbody>
        <tr>
            <td>
                <a href="${request.static_url('asjp:static/listss12.zip')}">012 [ZIP]</a>
            </td>
            <td>
                Wichmann, Søren, André Müller, Viveka Velupillai, Cecil H. Brown, Eric W. Holman, Pamela Brown, Matthias Urban, Sebastian Sauppe, Oleg Belyaev, Zarina Molochieva, Annkathrin Wett, Dik Bakker, Johann-Mattis List, Dmitry Egorov, Robert Mailhammer, and Helen Geyer. 2010. The ASJP Database (Version 12).
            </td>
        </tr>
        <tr>
            <td>
                <a href="${request.static_url('asjp:static/listss13.zip')}">013 [ZIP]</a>
            </td>
            <td>
                Wichmann, Søren, André Müller, Viveka Velupillai, Cecil H. Brown, Eric W. Holman, Pamela Brown, Sebastian Sauppe, Oleg Belyaev, Matthias Urban, Zarina Molochieva, Annkathrin Wett, Dik Bakker, Johann-Mattis List, Dmitry Egorov, Robert Mailhammer, David Beck, and Helen Geyer. 2010. The ASJP Database (version 13).
            </td>
        </tr>
        <tr>
            <td>
                <a href="${request.static_url('asjp:static/listss14.zip')}">014 [ZIP]</a>
            </td>
            <td>
                Wichmann, Søren, André Müller, Viveka Velupillai, Annkathrin Wett, Cecil H. Brown, Zarina Molochieva, Sebastian Sauppe, Eric W. Holman, Pamela Brown, Julia Bishoffberger, Dik Bakker, Johann-Mattis List, Dmitry Egorov, Oleg Belyaev, Matthias Urban, Robert Mailhammer, Helen Geyer, David Beck, Evgenia Korovina, Pattie Epps, Pilar Valenzuela, Anthony Grant, and Harald Hammarström. 2011. The ASJP Database (version 14).
            </td>
        </tr>
        <tr>
            <td>
                <a href="${request.static_url('asjp:static/listss15.zip')}">015 [ZIP]</a>
            </td>
            <td>
                Wichmann, Søren, André Müller, Viveka Velupillai, Annkathrin Wett, Cecil H. Brown, Zarina Molochieva, Julia Bishoffberger, Eric W. Holman, Sebastian Sauppe, Pamela Brown, Dik Bakker, Johann-Mattis List, Dmitry Egorov, Oleg Belyaev, Matthias Urban, Harald Hammarström, Agustina Carrizo, Robert Mailhammer, Helen Geyer, David Beck, Evgenia Korovina, Pattie Epps, Pilar Valenzuela, and Anthony Grant. 2012. The ASJP Database (version 15).
            </td>
        </tr>
        </tbody>
    </table>
</div>