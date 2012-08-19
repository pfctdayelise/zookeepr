<%inherit file="/base.mako" />

<h2>View funding type</h2>

<p>
   <b>Name:</b>
    ${ c.funding_type.name | h }
</p>

<p>
  <b>Active:</b> ${ h.yesno(c.funding_type.active) | n }
</p>

${ h.link_to('Edit', url=h.url_for(action='edit',id=c.funding_type.id)) } |
${ h.link_to('Back', url=h.url_for(action='index', id=None)) }
