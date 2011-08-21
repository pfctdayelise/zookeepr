<%namespace name="toolbox" file="/leftcol/toolbox.mako"/>
<%inherit file="view_base.mako" />

<%def name="toolbox_extra()">
  ${ parent.toolbox_extra() }
% if c.next_review_id:
  ${ toolbox.make_link('Skip!', url=h.url_for(controller='proposal', action='review', id=c.next_review_id)) }
% endif
</%def>


<%def name="heading()">
  Proposal Review - #${ c.proposal.id } - ${ c.proposal.title | h }
</%def>

${ h.form(h.url_for()) }

% if c.next_review_id:
${ toolbox.make_link('Skip!', url=h.url_for(controller='proposal', action='review', id=c.next_review_id)) }
% else:
<ul><li><em>Can't skip - you have reviewed all the other ${c.proposal.type.name }s!</em></li></ul>
% endif

<h3>Review</h3>
  <% reviewed_already = False %>
% for x in c.proposal.reviews:
%   if x.reviewer == c.signed_in_person:
<p>You have already reviewered this proposal. To modify your review, ${ h.link_to('click here', url=h.url_for(controller='review', action='edit', id=x.id)) }.</p>
        <% reviewed_already = True %>
        <% break %>
%   endif
% endfor
% if not reviewed_already:
<fieldset>
<legend>
Your opinion on this proposal.
</legend>

<div id="q1">
<p class="label"><span class="mandatory">*</span><b>What score do you give this proposal?</b></p>
<p class="entries">
${ h.radio('review.score', '-2', label="-2 (strong reject) I want this proposal to be rejected, and if asked to I will advocate for it to be rejected.") }
<br>
${ h.radio('review.score', '-1', label="-1 (reject) I want this proposal to be rejected") }
<br>
${ h.radio('review.score', '+1', label="+1 (accept) I want this proposal to be accepted") }
<br>
${ h.radio('review.score', '+2', label="+2 (strong accept) I want this proposal to be accepted, and if asked to I will advocate for it to be accepted.") }
</p>
</div>

% if len(c.streams) > 1:
<div id="q2">
<p class="label">
<b>What stream do you think this talk is most suitable for?</b>
</p>

<p>
${ h.select('review.stream', None, c.streams ) }
</p>
</div>
% else:
${ h.hidden('review.stream') }
% endif

% if len(h.lca_info['cfp_miniconf_list']) > 1 and c.proposal.proposal_type_id is not 2:
<div id="q3">
<p class="label">
<b>What miniconf would this talk be most suitable for, if it's not accepted?</b>
</p>

<p>
${ h.select('review.miniconf', None, [ (mc, mc) for mc in h.lca_info['cfp_miniconf_list']] ) }
</p>
</div>
% else:
${ h.hidden('review.miniconf') }
% endif

<p class="label"><b>Comments</b> (optional, readable by other reviewers, will not be shown to the submitter)
</p>
<p class="entries">
${ h.textarea('review.comment', cols="80", rows="10") }
</p>

</fieldset>

<p>
<span class="mandatory">*</span> - Mandatory field
</p>

<p class="submit">
${ h.submit('submit', 'Submit review and jump to next proposal!') }
</p>

% endif

<p>
% if c.next_review_id:
${ h.link_to('Skip!', url=h.url_for(controller='proposal', action='review', id=c.next_review_id)) } - 
% endif
${ h.link_to('Back to proposal list', url=h.url_for(controller='proposal', action='review_index')) }
</p>
${ h.end_form() }

<%def name="title()">
Reviewing proposal #${ c.proposal.id } - ${ parent.title() }
</%def>
