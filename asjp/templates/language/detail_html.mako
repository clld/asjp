<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "languages" %>
<%block name="title">${_('Language')} ${ctx.name}</%block>

<h2>${_('Language')} ${ctx.name}</h2>
<p>
    ${h.alt_representations(request, ctx)}
</p>
<p>
    Compiled by ${h.linked_contributors(request, ctx.wordlist)}
</p>
${request.get_datatable('values', h.models.Value, language=ctx).render()}

<%def name="sidebar()">
    <div style="margin-top: 5px;">
    ${util.codes(ctx)}
    </div>
    <br clear="both" />
    % if ctx.latitude is not None:
    <%util:well>
        ${request.map.render()}
        ${h.format_coordinates(ctx)}
        <table class="table table-condensed">
            <tbody>
                % if ctx.number_of_speakers:
                <tr>
                    <td>number of speakers</td>
                    <td>${"{:,}".format(ctx.number_of_speakers)}</td>
                </tr>
                % endif
                <tr>
                    <td>status</td>
                    <td>
                    % if ctx.recently_extinct or ctx.long_extinct:
                        extinct
                        % if ctx.year_of_extinction:
                        since ${ctx.year_of_extinction}
                        % endif
                    % else:
                        alive
                    % endif
                    </td>
                </tr>
            </tbody>
        </table>
    </%util:well>
    % endif
    <%util:well title="Classification">
        <dl>
        % for label, attr in [('WALS', 'wals'), ('', 'glottolog'), ('', 'ethnologue')]:
            % if getattr(ctx, 'classification_' + attr):
            <dt>${label or attr.capitalize()}</dt>
            <dd>${u.normalize_classification(getattr(ctx, 'classification_' + attr), attr).replace(', ' , ' > ')}</dd>
            % endif
        % endfor
        </dl>
    </%util:well>
    <%util:well title="Sources">
        ${util.sources_list(sorted(list(ctx.sources), key=lambda s: s.name))}
    </%util:well>
</%def>
