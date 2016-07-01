<%inherit file="app.mako"/>

##
## define app-level blocks:
##
<%block name="brand">
    <a href="${request.resource_url(request.dataset)}" class="brand">ASJP</a>
</%block>

<%block name="footer">
    <div class="row-fluid" style="padding-top: 15px; border-top: 1px solid black;">
        <div class="span3">
            <a href="${request.dataset.publisher_url}"
               title="${request.dataset.publisher_name}, ${request.dataset.publisher_place}">
                <img width="80" src="${request.static_url(request.registry.settings['clld.publisher_logo'])}" />
            </a>
        </div>
        <div class="span6" style="text-align: center;">
            ${request.dataset.formatted_name()}
            is licensed under a
            <a rel="license" href="${request.dataset.license}">
                ${request.dataset.jsondata.get('license_name', request.dataset.license)}
            </a>.
            Its development has been partially funded by the Max Planck Society for the Advancement of Science and
            the European Research Council (ERC advanced grant MesAndLin(g)k, proj. no. 295918).
            <br />
        </div>
        <div class="span3" style="text-align: right;">
            <a href="${request.route_url('legal')}">disclaimer</a>
            <br/>
            % if request.registry.settings.get('clld.github_repos'):
                <a href="https://github.com/${request.registry.settings['clld.github_repos']}">
                    <i class="icon-share">&nbsp;</i>
                    Application source on<br/>
                    <img height="25" src="${request.static_url('clld:web/static/images/GitHub_Logo.png')}" />
                </a>
            % endif
        </div>
    </div>
</%block>

${next.body()}
