<%inherit file="home_comp.mako"/>

<h3>Software</h3>

<ul>
    % for li in files:
    ${li|n}
    % endfor
	<li>List, Johann-Mattis. 2013. ${h.external_link("https://gist.github.com/LinguList/7612513", label="SCA Cognate Detection Applied to ASJP Data.")}
</ul>