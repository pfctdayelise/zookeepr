<%inherit file="/base.mako" />
<h2>
Your account has already been confirmed.
</h2>

<p>
Please ${ h.link_to('sign in', url=h.url_for(controller='/person', action='signin')) } to your account.
</p>

<p>
Don't forget to sign up to the <a href="http://lists.linux.org.au/listinfo/lca-announce">lca-announce@linux.org.au</a> and <a href="http://lists.lca2011.linux.org.au/lca2011-chat">lca2011-chat@lists.lca2011.linux.org.au</a> mailing list!
</p>
