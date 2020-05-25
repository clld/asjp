<%inherit file="home_comp.mako"/>
<%namespace name="clldmpgutil" file="clldmpg_util.mako"/>
<%namespace name="util" file="util.mako"/>


<h3>Downloads</h3>
<div class="alert-info alert">
    This web application serves the latest released version of
    <a href="https://doi.org/10.5281/zenodo.3835822">
        <img src="https://zenodo.org/badge/DOI/10.5281/zenodo.3835822.svg" alt="DOI">
    </a>.
    The ASJP database in ASJP's txt format is included in the zip file provided as download at Zenodo
    under the directory path <span style="font-family: monospace">raw/lists.txt</span>.
</div>

    <h4>Current and earlier versions of the ASJP Database</h4>
    <table class="table table-nonfluid">
        <thead>
        <tr><th>Version no.</th><th>Year</th><th>DOI</th><th>Cite as</th></tr>
        </thead>
        <tbody>
        <tr>
            <td>19</td>
            <td>2019</td>
            <td>
                <a href="https://doi.org/10.5281/zenodo.3843469">10.5281/zenodo.3843469</a>
            </td>
            <td>
                Wichmann, Søren, Eric W. Holman, and Cecil H. Brown (eds.). 2019. The ASJP Database (version 19).
            </td>
        </tr>
        <tr>
            <td>18</td>
            <td>2018</td>
            <td>
     <a href="https://doi.org/10.5281/zenodo.3835952">10.5281/zenodo.3835952</a>
            </td>
            <td>
                Wichmann, Søren, Eric W. Holman, and Cecil H. Brown (eds.). 2018. The ASJP Database (version 18).
            </td>
        </tr>
        <tr>
            <td>17</td>
            <td>2016</td>
            <td>
                <a href="https://doi.org/10.5281/zenodo.3835942">10.5281/zenodo.3835942</a>
            </td>
            <td>
                Wichmann, Søren, Eric W. Holman, and Cecil H. Brown (eds.). 2016. The ASJP Database (version 17).
            </td>
        </tr>
        <tr>
            <td>16</td>
            <td>2013</td>
            <td>
                <a href="https://doi.org/10.5281/zenodo.3835925">10.5281/zenodo.3835925</a>
            </td>
            <td>
                Wichmann, Søren, André Müller, Annkathrin Wett, Viveka Velupillai, Julia Bischoffberger, Cecil H. Brown, Eric W. Holman, Sebastian Sauppe, Zarina Molochieva, Pamela Brown, Harald Hammarström, Oleg Belyaev, Johann-Mattis List, Dik Bakker, Dmitry Egorov, Matthias Urban, Robert Mailhammer, Agustina Carrizo, Matthew S. Dryer, Evgenia Korovina, David Beck, Helen Geyer, Pattie Epps, Anthony Grant, and Pilar Valenzuela. 2013. The ASJP Database (version 16).
            </td>
        </tr>
        <tr>
            <td>15</td>
            <td>2012</td>
            <td>
                <a href="https://doi.org/10.5281/zenodo.3835901">10.5281/zenodo.3835901</a>
            </td>
            <td>
                Wichmann, Søren, André Müller, Viveka Velupillai, Annkathrin Wett, Cecil H. Brown, Zarina Molochieva, Julia Bishoffberger, Eric W. Holman, Sebastian Sauppe, Pamela Brown, Dik Bakker, Johann-Mattis List, Dmitry Egorov, Oleg Belyaev, Matthias Urban, Harald Hammarström, Agustina Carrizo, Robert Mailhammer, Helen Geyer, David Beck, Evgenia Korovina, Pattie Epps, Pilar Valenzuela, and Anthony Grant. 2012. The ASJP Database (version 15).
            </td>
        </tr>
        <tr>
            <td>14</td>
            <td>2011</td>
            <td>
                <a href="https://doi.org/10.5281/zenodo.3835887">10.5281/zenodo.3835887</a>
            </td>
            <td>
                Wichmann, Søren, André Müller, Viveka Velupillai, Annkathrin Wett, Cecil H. Brown, Zarina Molochieva, Sebastian Sauppe, Eric W. Holman, Pamela Brown, Julia Bishoffberger, Dik Bakker, Johann-Mattis List, Dmitry Egorov, Oleg Belyaev, Matthias Urban, Robert Mailhammer, Helen Geyer, David Beck, Evgenia Korovina, Pattie Epps, Pilar Valenzuela, Anthony Grant, and Harald Hammarström. 2011. The ASJP Database (version 14).
            </td>
        </tr>
        <tr>
            <td>13</td>
            <td>2010</td>
            <td>
                <a href="https://doi.org/10.5281/zenodo.3835872">10.5281/zenodo.3835872</a>
            </td>
            <td>
                Wichmann, Søren, André Müller, Viveka Velupillai, Cecil H. Brown, Eric W. Holman, Pamela Brown, Sebastian Sauppe, Oleg Belyaev, Matthias Urban, Zarina Molochieva, Annkathrin Wett, Dik Bakker, Johann-Mattis List, Dmitry Egorov, Robert Mailhammer, David Beck, and Helen Geyer. 2010. The ASJP Database (version 13).
            </td>
        </tr>
        <tr>
            <td>12</td>
            <td>2010</td>
            <td>
                <a href="https://doi.org/10.5281/zenodo.3835823">10.5281/zenodo.3835823</a>
            </td>
            <td>
                Wichmann, Søren, André Müller, Viveka Velupillai, Cecil H. Brown, Eric W. Holman, Pamela Brown, Matthias Urban, Sebastian Sauppe, Oleg Belyaev, Zarina Molochieva, Annkathrin Wett, Dik Bakker, Johann-Mattis List, Dmitry Egorov, Robert Mailhammer, and Helen Geyer. 2010. The ASJP Database (Version 12).
            </td>
        </tr>
        </tbody>
    </table>
    <h4>Current and earlier versions of the ASJP World Language Tree of Lexical Similarity</h4>
    <table class="table">
        <thead>
            <tr><th>Version no.</th><th>Year</th><th>Cite as</th></tr>
        </thead>
        <tbody>
            <tr>
                <td>
                    <a href="${request.static_url('asjp:static/WorldLanguageTree-001.pdf')}">001 [PDF]</a>
                </td>
                <td>2009</td>
                <td>
                    André Müller, Viveka Velupillai, Søren Wichmann, Cecil H. Brown, Pamela Brown, Eric W. Holman, Dik Bakker, Oleg Belyaev, Dmitri Egorov, Robert Mailhammer, Anthony Grant, and Kofi Yakpo. 2009. ASJP World Language Tree: Version 1 (April 2009).
                </td>
            </tr>
            <tr>
                <td>
                    <a href="${request.static_url('asjp:static/WorldLanguageTree-002.pdf')}">002 [PDF]</a>
                </td>
                <td>2009</td>
                <td>
                    André Müller, Viveka Velupillai, Søren Wichmann, Cecil H. Brown, Pamela Brown, Eric W. Holman, Dik Bakker, Oleg Belyaev, Dmitri Egorov, Robert Mailhammer, Anthony Grant, and Kofi Yakpo. 2009. ASJP World Language Tree of Lexical Similarity: Version 2 (April 2009).
                </td>
            </tr>
            <tr>
                <td>
                    <a href="${request.static_url('asjp:static/WorldLanguageTree-003.pdf')}">003 [PDF]</a>
                </td>
                <td>2010</td>
                <td>
                    Müller, André, Søren Wichmann, Viveka Velupillai, Cecil H. Brown, Pamela Brown, Sebastian Sauppe, Eric W. Holman, Dik Bakker, Johann-Mattis List, Dmitri Egorov, Oleg Belyaev, Robert Mailhammer, Matthias Urban, Helen Geyer, and Anthony Grant. 2010. ASJP World Language Tree of Lexical Similarity: Version 3 (July 2010).
                </td>
            </tr>
            <tr>
                <td>
                    <a href="${request.static_url('asjp:static/WorldLanguageTree-004.zip')}">004 [ZIP]</a>
                </td>
                <td>2013</td>
                <td>
                    Müller, André, Viveka Velupillai, Søren Wichmann, Cecil H. Brown, Eric W. Holman, Sebastian Sauppe, Pamela Brown, Harald Hammarström, Oleg Belyaev, Johann-Mattis List, Dik Bakker, Dmitri Egorov, Matthias Urban, Robert Mailhammer, Matthew S. Dryer, Evgenia Korovina, David Beck, Helen Geyer, Pattie Epps, Anthony Grant, and Pilar Valenzuela. 2013. ASJP World Language Trees of Lexical Similarity: Version 4 (October 2013).
                </td>
            </tr>
        </tbody>
    </table>
