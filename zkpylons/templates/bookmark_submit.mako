<%def name="bookmark_submit(url, title='')">
<div class="bookmark_submit">
<%
 if len(title) == 0:
    title = h.lca_info["event_byline"]
 endif
 twit_title = title + ': ';
%>

  <a href="http://del.icio.us/post?url=${ url }"><img src="/images/sm_icons/delicious.png" width="16" height="16" alt="[D]" title="Submit to Del.icio.us"></a>
  <a href="http://digg.com/submit?phase=2&amp;url=${ url }"><img src="/images/sm_icons/digg.png" width="16" height="14" alt="[Digg]" title="Submit to Digg"></a>
  <a href="http://facebook.com/sharer.php?t=${ h.url_escape(title + ' ' + h.lca_info["event_hashtag"]) }&u=${ url }"><img src="/images/sm_icons/facebook.png" width="16" height="16" alt="[SU]" title="Set status on Facebook"></a>
  <a href="http://reddit.com/submit?url=${ url }"><img src="/images/sm_icons/reddit.png" width="20" height="17" alt="[R]" title="Submit to Reddit"></a>
  <a href="http://www.stumbleupon.com/submit?url=${ url }"><img src="/images/sm_icons/stumble.png" width="16" height="16" alt="[SU]" title="Submit to Stumble Upon"></a>
  <a href="http://twitter.com/home?status=${ h.url_escape(twit_title + url + ' ' + h.lca_info["event_hashtag"]) }"><img src="/images/sm_icons/twitter.png" width="16" height="16" alt="[SU]" title="Set status on Twitter"></a>
</div>
</%def>

