<%inherit file="home_comp.mako"/>
<%namespace name="util" file="util.mako"/>

<%def name="sidebar()">
    <%util:well>
        <ul class="unstyled">
            <li><a href="#dl-database">How to download the entire ASJP database</a></li>
            <li><a href="#dl-selection">How to download a selection of wordlists</a></li>
            <li><a href="#desc">General description of the ASJP database of wordlists</a></li>
            <li><a href="#matrix">How to get a matrix of ASJP distances</a></li>
            <li><a href="#software">More detail on the software and input file format</a></li>
            <li><a href="#refs">References</a></li>
        </ul>
    </%util:well>
</%def>

<h2>Instructions</h2>

<%util:section title="How to download the entire ASJP database" id="dl-database">
    <ol>
        <li>Click on <a href="${request.route_url('languages')}">Wordlists</a>.</li>
        <li>Click on the download icon ${h.icon('download-alt')} near the upper right corner of the screen.</li>
        <li>In the menu, click on ASJP text format and wait 30 sec or so.</li>
    </ol>
    <p>Alternatively,</p>
    <ol>
        <li>Click on <a href="${request.route_url('download')}">Download</a>.</li>
        <li>Click on 017[ZIP].</li>
        <li>Click on OK.</li>
        <li>Double click on listss16 and wait 30 sec or so.</li>
    </ol>
    <p>
        Either way, you should get the complete database, set up to run on ASJP programs. Now you can
        copy and paste whatever you want of this into a data file of your own. To find a particular
        language in the database, search for its ISO 639-3-code preceded by three spaces. The ISO
        639-3-code sits to the far right in the second line of each word list. There may be more than
        one list with the same ISO 639-3-code, representing different dialects or sources.
    </p>
</%util:section>
<%util:section title="How to download a selection of wordlists" id="dl-selection">
    <p>
        Click on <a href="${request.route_url('languages')}">Wordlists</a>.
        In the search fields below the column headers you can enter your search criteria. The ISO 639-3 field
        (but not the Glottocode or WALS fields) allows for entering multiple codes separated by spaces.
        The Latitude, Longitude, Number of speakers and Year of extinction fields allow for simple
        Boolean expressions. For instance, &gt;1000000 in the Number of speakers field will produce all
        languages with more than a million speakers. In the Classification Ethnologue and the Classification
        Glottolog fields you can insert a family or a subgroup of a phylogeny. For instance, inserting
        Indo-European,Baltic into Classification Ethnologue will give you Latvian and Lithuanian.
        Clicking on the download icon and selecting ASJP text format, produces a file for these languages
        which can either be copied and pasted or saved using the browser’s file save option.
    </p>
</%util:section>
<%util:section title="General description of the ASJP database of wordlists" id="desc">
    <p>
        Whether you have downloaded the entire database or a subset, the general format is the same, and 
        this is described here.
    </p>
    <p>
        The first line is specific to ASJP software. For users of that software, the 2 in col. 6 is the
        maximum number of synonyms read for each item, the number in cols. 11-12 indicates that wordlists
        with at least that number of attested items are used, and the number in cols. 15-18 is a date that
        can specify which lists are used (if it’s 0, all lists with enough attested items are used).
    </p>
    <p>
        The next line gives the format for reading the immediately following list. The list itself consists
        of the 40 most stable items, as determined by
        <a href="#holman-et-al-2008">Holman et al. (2008)</a>, in the 100-item list of
        <a href="#swadesh-1955">Swadesh (1955)</a>. Most of the wordlists in the database contain these 40 items,
        or as many of them as are attested in the sources. About 300 wordlists contain as many items as are
        attested from the full 100-item Swadesh list. The English names of the items are less important than the
        preceding numbers, which are used to identify the items in the wordlists.
    </p>
    <p>
        The next list consists of the ASJP code symbols that are used to transcribe the wordlists. These are
        described by <a href="#brown-et-al-2008">Brown et al. (2008)</a>.
    </p>
    <p>
        Then there is a wordlist for each language, on consecutive lines. In the full database, lists are
        ordered according to the classification in WALS (<a href="#wals">Haspelmath et al. 2005</a>). Families are ordered
        geographically, genera are ordered alphabetically within families, and languages are ordered
        alphabetically within genera. The format of each list, including the two first lines consisting of
        metadata, is described below in the section <a href="#software">More detail on the software and input file format</a>.
    </p>
</%util:section>
<%util:section title="How to get a matrix of ASJP distances" id="matrix">
    <p>
        Download the entire database and make a selection or download a selection as described above.
        The file must contain all the stuff before the first list in the ASJP database, including the
        blank lines. It must also have a line at the end containing at least 5 blank characters
        (&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;), but no other blank lines between or within lists. You can now apply
        our software. This is downloaded and installed as follows.
    </p>
    <ol>
        <li>Click on <a href="${request.route_url('software')}">Software</a>.</li>
        <li>Click on Programs for calculating ASJP distance matrices (Holman 2011c).</li>
        <li>Unzip and save the .exe files in the same folder that your data file is in.</li>
    </ol>
    <p>
        There is also an Instructions file, but all the instructions for the programs described
        here are also contained in the present document.
        There are different programs:
        <span style="font-family: monospace">asjp62</span>,
        <span style="font-family: monospace">asjp62x</span>,
        <span style="font-family: monospace">asjp62e</span>. To just produce a distance matrix
        <span style="font-family: monospace">asjp62</span> can be used. The other programs are described in the next section.
    </p>
    <p>
        You run the program in the DOS Command Prompt as follows. Type:
    </p>
    <pre>
        asjp62 &lt; yourdata.txt &gt; output</pre>
    <p>
        where ‘yourdata’ is the name of your data file and ‘output’ is the name of your output file. Press Enter
        and wait a few seconds to a few hours, depending on the size of your data file.
    </p>
    <p>
        The output should be a matrix of distances between the lists in the data file. By the default settings
    </p>
    <ul>
        <li>words identified in the database as loans aren’t used in calculating distances;</li>
        <li>
            if a list has two synonymous words for a given item, both are used and the distance is the average
            of the distances based on each synonym;
        </li>
        <li>
            if a list has words for fewer than 28 items (not counting loanwords), or if the list refers to a
            language that went extinct before 1700 CE, distances involving that list aren’t calculated.
        </li>
    </ul>
    <p>
        To change these options, consult the next section.
    </p>
</%util:section>
<%util:section title="More detail on the software and input file format" id="software">
    <p>
        The programs described here calculate LDND, as defined by
        <a href="#bakker-et-al-2009">Bakker et al. (2009)</a>, between pairs of languages.
        The programs all use the same input and produce slightly different output.
    </p>
    <ul class="bullet_list">
        <li>
            <span style="font-family: monospace">asjp62</span>
            produces a matrix of LDND with rows and columns labeled by the language names.
        </li>
        <li>
            <span style="font-family: monospace">asjp62x</span> produces the same matrix in a
            format appropriate for use as input to the MEGA6 phylogeny package
            (<a href="#tamura-et-al-2013">Tamura et al. 2013</a>). It outputs distances in percentages
            with two decimal points but with the dot removed
            (alternatively the numbers can be interpreted as multiplied by 100). This is a way of saving space in the
            matrix which, with the current number of languages in the database, would otherwise be too large for MEGA6
            (<a href="#tamura-et-al-2013">Tamura et al. 2013</a>).
        </li>
        <li>
            <span style="font-family: monospace">asjp62e</span> produces 1-LDND for pairs of languages within
            taxonomic groups, with each pair on a separate
            line in a format appropriate for pasting into spreadsheet software like Excel.
        </li>
    </ul>
    <p>
        To run a program, get the MS-DOS command prompt, type a command of the form
    </p>
    <pre>
        program &lt; input &gt; output</pre>
    <p>
        and then press Enter. For example, the command
        </p>
    <pre>
        asjp62x &lt; input.txt &gt; output62x.txt</pre>
    <p>
        will run
        <span style="font-family: monospace">asjp62x</span> on <span style="font-family: monospace">input.txt</span>
        to produce <span style="font-family: monospace">output62x.txt</span>. The computer may add the line
    </p>
    <blockquote>
Stop - Program terminated.
    </blockquote>
    <p>
        to the end of the output, but this can be deleted before the output is used further.
    </p>
    <p>
        The input file must obey the following general rules.
    </p>
    <ul>
        <li>
            The first line is in fixed format so the columns are important.
            <dl>
                <dt>Col. 6:</dt>
                <dd>maximum number of synonyms read for each item (1 or 2).</dd>
                <dt>Col. 11-12:</dt>
                <dd>
                    minimum number of attested items in lists, up to 100; lists with fewer
                    attested items are ignored.
                </dd>
                <dt>Col. 15-18:</dt>
                <dd>
                    if this number is 0, all lists are read; if it’s a positive number, it’s
                    interpreted as a date and lists from languages extinct before that date are ignored.
                </dd>
                <dt>Col. 24:</dt>
                <dd>
                    if this is a number other than 0, transcribed words and phrases preceded by % are ignored,
                    which allows loans to be excluded if they are identified by %.
                </dd>
                <dt>Col. 30:</dt>
                <dd>
                    Taxonomic rank of groups within which similarities are calculated by
                    <span style="font-family: monospace">asjp62e</span>: 3 = families, 2 = genera.
                    Only <span style="font-family: monospace">asjp62e</span> uses this information;
                    <span style="font-family: monospace">asjp62</span> and
                    <span style="font-family: monospace">asjp62x</span> ignore it.
                    The ASJP database uses the families and genera defined in WALS
                    (<a href="#wals">Haspelmath et al. 2005</a>)
                    but the computer will accept whatever definition is specified for the languages as
                    described below for Col. 2 in the second line of metadata.
                </dd>
            </dl>
        </li>
        <li>
            The next line gives the format for reading the item numbers below it. The programs described here
            ignore the item names so the format in the example could just as well be I4.
        </li>
        <li>
            The next set of lines gives the item numbers that will be used. There is one line for each item in
            the list. The item numbers must be between 1 and 100 inclusive, but they don't have to be consecutive
            or listed in numerical order. For I4 format, the numbers must be in Cols. 1-4, right justified.
            Items with numbers other than those listed here aren’t used in calculating LDND. The item names in
            the example are just for convenience.
        </li>
        <li>
            There must be a blank line after the item list. Press the space bar a few times to give the computer
            something to read. This line tells the computer that the item list is finished.
        </li>
        <li>
            The next set of lines gives the ASJPcode symbols, one per line in Col. 1, in any order.
            As an alternative to ASJPcode, any ascii symbols can be used; there can be up to 100 different symbols.
            Symbols not on this list aren’t used in calculating LDND (except for the four modifier symbols, which
            are described in <a href="#brown-et-al-2008">Brown et al. 2008</a>).
        </li>
        <li>
            There must be two blank lines after the symbol list.
        </li>
        <li>
            Then there is a wordlist for each language, on consecutive lines, consisting of two lines of metadata
            and then the wordlist proper. The metadata format is described below.
        </li>
        <li>
            The first line for each list gives the name of the language followed within curly brackets by its
            position in three classifications, without any blank spaces. The name is taken from the source of
            the list; it never starts with a number or a blank. Between { and | is the classification of the
            language in WALS. It’s of the form Fam.GENUS, with the family name abbreviated and the genus name
            spelled out. Between | and @ is the classification of the language in Ethnologue (<a href="#lewis-et-al-2014">Lewis et al. 2014</a>),
            and between @ and } is the classification in Glottolog (<a href="#glottolog">Hammarström et al. 2014</a>). Names of taxonomic
            groups and subgroups are separated by commas and ordered from most inclusive to least inclusive.
            Languages not in a given classification are classified from information in the source for the list.
            If this information is insufficient for WALS, the family and genus are called Unknown. If it’s
            insufficient for Ethnologue or Glottolog, the sequence of subgroups is continued only as far as the
            information permits, including in some cases no groups at all.
        </li>
        <li>
            The second line gives properties of the languages, again in fixed format so the columns are important.
            <dl>
                <dt>Col. 2:</dt>
                <dd>
                    3 if the language is the first one in a new family, 2 if it’s the first language in a new genus,
                    1 otherwise.
                </dd>
                <dt>Col. 4-10:</dt>
                <dd>
                    latitude in degrees and hundredths of a degree; minus means South. The programs described here
                    don’t use this information.
                </dd>
                <dt>Col. 12-18:</dt>
                <dd>
                    longitude in degrees and hundredths of a degree; minus means West. The programs described here
                    don’t use this information.
                </dd>
                <dt>Col. 19-30:</dt>
                <dd>
                    number of speakers, from Ethnologue (<a href="#lewis-et-al-2014">Lewis et al. 2014</a>);
                    0 if the number of speakers is unknown; -1 if the language is recently extinct;
                    -2 if the language is long extinct; or if the approximate date of extinction is known,
                    the date is preceded by a minus sign. If there is a date in the first line of the entire file,
                    lists with earlier extinction dates here are ignored, as are lists with -2; otherwise, all lists are used.
                </dd>
                <dt>Col. 34-36:</dt>
                <dd>three-letter WALS code, if any. The programs described here don’t use this information.</dd>
                <dt>Col. 40-42:</dt>
                <dd>three-letter ISO code from Ethnologue, if any. The programs described here don’t use this information.</dd>
            </dl>
        </li>
        <li>
            Each of the next lines refers to an item in the list, until the next language begins.
            Items can be in any order. The line must begin with the item number, starting in Col. 1,
            left justified. The next column after the number can be anything except a tab.
            The program then ignores everything until it reaches a tab; this part of the line can be used
            for the name of the item. After the tab is the transcribed word or phrase; words in a phrase
            are separated by a space, which is ignored in the calculations; synonyms are separated by a comma.
            XXX here means that the item isn’t attested for the language; alternatively, unattested items can
            be omitted from the list. The end of the transcription is indicated by a space and then //.
            Two consecutive spaces also signal the end of the transcription.
        </li>
        <li>
            There must be a blank line after the last list.
        </li>
    </ul>
</%util:section>
<%util:section title="References" id="refs">
    <p id="bakker-et-al-2009">
        Bakker, Dik, André Müller, Viveka Velupillai, Søren Wichmann, Cecil H. Brown, Pamela Brown, Dmitry Egorov, Robert Mailhammer, Anthony Grant, and Eric W. Holman. 2009.
        Adding Typology to Lexicostatistics: A Combined Approach to Language Classification.
        <i>Linguistic Typology</i> 13.167-179.
    </p>
    <p id="brown-et-al-2008">
        Brown, Cecil H., Eric W. Holman, Søren Wichmann, and Viveka Vilupillai. 2008.
        Automated classification of the world’s languages: a description of the method and preliminary results.
        <i>STUF – Language Typology and Universals</i>:285-308.
    </p>
    <p id="glottolog">
        Hammarström, Harald, Robert Forkel, Martin Haspelmath, and Sebastian Nordhoff. 2014.
        Glottolog 2.3. Leipzig: Max Planck Institute for Evolutionary Anthropology.
        (${h.external_link('http://glottolog.org')})
    </p>
    <p id="wals">
        Haspelmath, Martin, Matthew Dryer, David Gil, and Bernard Comrie (eds.). 2005.
        <i>The World Atlas of Language Structures</i>.
        Oxford: Oxford University Press.
        (${h.external_link('http://wals.info/')})
    </p>
    <p id="holman-et-al-2008">
        Holman, Eric W., Søren Wichmann, Cecil H. Brown, Viveka Velupillai, André Müller, Pamela Brown, and Dik Bakker. 2008.
        Explorations in automated language comparison.
        <i>Folia Linguistica</i> 42:331-354.
    </p>
    <p id="lewis-et-al-2014">
        Lewis, M. Paul, Gary F. Simons, and Charles D. Fennig (eds.). 2014.
        <i>Ethnologue: Languages of the World, Seventeenth edition</i>.
        Dallas, Texas: SIL International.
        Online version: ${h.external_link('http://www.ethnologue.com')}.
    </p>
    <p id="tamura-et-al-2013">
        Tamura, K., G. Stecher, D. Peterson, A. Filipski, and S. Kumar. 2013.
        MEGA6: Molecular Evolutionary Genetics Analysis Version 6.0.
        ${h.external_link('http://mbe.oxfordjournals.org/content/30/12/2725.abstract.html?etoc', label='Molecular Biology and Evolution')}
        30:2725-2729.
    </p>
    <p id="swadesh-1955">
        Swadesh, Morris. 1955. Towards greater accuracy in lexicostatistic dating.
        <i>International Journal of American Linguistics</i>: 121-137.
    </p>
</%util:section>
