<%inherit file="/base.mako" />
<h2>Expired!</h2>

<p>
This password recovery session has expired. Please send in another request to have your password set.
</p>

<p>
If you believe this to be an error, please contact ${ h.contact_email() }.
</p>

<p><a href="${ h.url_for('home') }">Return to login page</a>
