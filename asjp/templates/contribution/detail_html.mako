<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "contributions" %>

<h2>${_('Contribution')} ${ctx.name}</h2>

${request.get_datatable('values', h.models.Value, contribution=ctx).render()}

<%def name="sidebar()">
    <%util:well title="Compiler">
        ${h.linked_contributors(request, ctx)}
        ${h.cite_button(request, ctx)}
    </%util:well>
    <%util:well title="Language">
        ${h.link(request, ctx.language)}
    </%util:well>
    <%util:well title="Sources">
        ${util.sources_list(sorted(list(ctx.language.sources), key=lambda s: s.name))}
    </%util:well>
</%def>
