<%inherit file="/base.mako" />
<h2>
Your account has already been confirmed.
</h2>

<p>
Please ${ h.link_to('sign in', url=h.url_for(controller='/person', action='signin')) } to your account.
</p>

<p>
Don't forget to sign up to the <a href="${ h.lca_info['mailing_list_announce_url'] }">${ h.lca_info['mailing_list_announce_addr'] }</a> and <a href="${ h.lca_info['mailing_list_chat_url'] }">${ h.lca_info['mailing_list_chat_addr'] }</a> mailing list!
</p>
