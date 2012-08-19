<% day = 'monday' %>
<% miniconfs = [8, 157, 9, 49, 83, 116, 201, 26] %>
<% contents = '' %>
% for mid in miniconfs:
<%   miniconf = c.get_talk(mid) %>
<%   contents += '<li><a href="#' + day + '_' + h.computer_title(miniconf.title) + '">' + miniconf.title + '</li>' %>
% endfor

<div class="contents">
<h3>Monday's Miniconfs</h3>
<ul>
${ contents }
</ul>
</div>

% for mid in miniconfs:
<%include file="miniconf_link.mako", day=day, miniconf_id=mid />
% endfor
