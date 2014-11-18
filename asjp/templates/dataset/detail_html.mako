<%inherit file="../home_comp.mako"/>

<%def name="sidebar()">
    <div class="well">
        <h3>Sidebar</h3>
        <p>
            Content
        </p>
    </div>
</%def>

<div style="float: left; padding: 20px;">
<img width="200" height="200" src="${request.static_url('asjp:static/logo_asjp.gif')}" class="image"/>
</div>

<h2>${request.dataset.description}</h2>


How to cite:

Wichmann, Søren, André Müller, Annkathrin Wett, Viveka Velupillai, Julia Bischoffberger, Cecil H. Brown, Eric W. Holman, Sebastian Sauppe, Zarina Molochieva, Pamela Brown, Harald Hammarström, Oleg Belyaev, Johann-Mattis List, Dik Bakker, Dmitry Egorov, Matthias Urban, Robert Mailhammer, Agustina Carrizo, Matthew S. Dryer, Evgenia Korovina, David Beck, Helen Geyer, Pattie Epps, Anthony Grant, and Pilar Valenzuela. 2013. The ASJP Database (version 16).


#
# stats:
# THE FOLLOWING STATISTICS ONLY CONCERN 40-ITEM LISTS AND THE SUBSET OF THE 328 100-ITEM LISTS PERTAINING TO THE 40 STANDARD ASJP ITEMS

#unique language names:  6895

#Ethnologue families:  223

#Glottolog families:  381

#languages with unique ISO codes:  4424  match [a-z]{3}!

asjp=# select count(*) from (select distinct name from identifier where type = 'iso639-3') as s;
-[ RECORD 1 ]
count | 4401

#words in the database (not counting synonyms):  238976 and counting synonyms: ...
