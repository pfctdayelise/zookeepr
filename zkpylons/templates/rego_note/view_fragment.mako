<p><b>For registration:</b> </p>
<p><b>By:</b> ${ h.link_to(c.rego_note.rego.person.firstname + ' ' +
c.rego_note.rego.person.lastname, h.url_for(controller='person',
action='view', id=c.rego_note.rego.person.id)) },
${ h.link_to('View Registration', h.url_for(controller='registration', action='view', id=c.rego_note.rego.id)) }</p>

<p><b>Note:</b> ${ c.rego_note.note }</p>

<p>${ h.link_to('Edit', h.url_for(controller='rego_note', action='edit',
id=c.rego_note.id)) } | ${ h.link_to('Back', h.url_for(controller='rego_note', action='index')) }</p>

<%def name="title()">
View note - ${ parent.title() }
</%def>
