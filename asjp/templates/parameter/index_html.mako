<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "parameters" %>
<%block name="title">${_('Parameters')}</%block>

<h2>${title()}</h2>
<p>
    Counterparts of the 40 boldfaced meanings can be obtained here for all
    <a href="${request.route_url('languages')}">doculects</a> in the database, to the
    extent that they are attested. For a
    few hundred doculects the remaining items on the
    ${h.external_link('http://concepticon.clld.org/contributions/Swadesh-1955-100', label='Swadesh list')}
    are also included (normal font).
</p>
<ul class="unstyled inline">
% for p in request.db.query(h.models.Parameter).order_by(h.models.Parameter.pk):
    <li>
        % if p.core:
        <strong>${h.link(request, p)}</strong>
        % else:
        ${h.link(request, p)}
        % endif
    </li>
% endfor
</ul>
