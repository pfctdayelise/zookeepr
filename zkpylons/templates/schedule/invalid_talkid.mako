<%inherit file="/base.mako" />

<h2>Error: scheduled talk not found</h2>

<p>Could not find the talk/miniconf you asked for:
<span class="error-message">talk_id=${ c.talk_id }</span></p>

<p>Please <a href="mailto:${ c.webmaster_email }">email
us</a> with a copy of this page if you think that this should not
happen.</p>

<p>
% if c.day is None:
    <a href="/schedule/${ c.day }">
% else:
    <a href="/schedule">
% endif
&lt;-- Back to schedule</a></p>
