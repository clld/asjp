<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "sources" %>
<%block name="title">${_('Sources')}</%block>

<h2>${_('Sources')}</h2>
<p>
    This page, which is still partly under construction, provides sources
    for the lexical data. The general source for speaker numbers is
    ${h.external_link('http://www.ethnologue.com/', label='Ethnologue')}.
</p>
<div>
    ${ctx.render()}
</div>
