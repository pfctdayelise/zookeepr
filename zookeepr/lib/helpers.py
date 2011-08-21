"""Helper functions

Consists of functions to typically be used within templates, but also
available to Controllers. This module is available to templates as 'h'.
"""
# Import helpers as desired, or define your own, ie:
#from webhelpers.html.tags import checkbox, password

from webhelpers.html import escape, HTML, literal, url_escape
from webhelpers.html.tags import *
from webhelpers.text import *
import webhelpers.constants

try:
    from webhelpers.pylonslib import secure_form
except:
    from webhelpers.html.secure_form import secure_form

from lxml.html.clean import Cleaner

import webhelpers.util as util

from routes import request_config
from routes.util import url_for as pylons_url_for

from pylons import config, request, session

import os.path, random, array

from zookeepr.lib import auth

from zookeepr.model import Person

from zookeepr.config.lca_info import lca_info, lca_rego, lca_menu, lca_submenus
from zookeepr.config.zookeepr_config import file_paths

from sqlalchemy.orm.util import object_mapper

import itertools, re, Image
from glob import glob

def iterdict(items):
    return dict(items=items, iter=itertools.cycle(items))

def cycle(*args, **kargs):
    """
    Return the next cycle of the given list.

    Everytime ``cycle`` is called, the value returned will be the next.
    item in the list passed to it. This list is reset on every request,.
    but can also be reset by calling ``reset_cycle()``.

    You may specify the list as either arguments, or as a single list.
    argument.

    This can be used to alternate classes for table rows::

        # In Myghty...
        % for item in items:
        <tr class="<% cycle("even", "odd") %>">
            ... use item ...
        </tr>
        % #endfor

    You can use named cycles to prevent clashes in nested loops. You'll
    have to reset the inner cycle, manually::

        % for item in items:
        <tr class="<% cycle("even", "odd", name="row_class") %>
            <td>
        %     for value in item.values:
                <span style="color:'<% cycle("red", "green", "blue",
                                             name="colors") %>'">
                            item
                </span>
        %     #endfor
            <% reset_cycle("colors") %>
            </td>
        </tr>
        % #endfor
    """
    if len(args) > 1:
        items = args
    else:
        items = args[0]
    name = kargs.get('name', 'default')
    cycles = request_config().environ.setdefault('railshelpers.cycles', {})

    cycle = cycles.setdefault(name, iterdict(items))

    if cycles[name].get('items') != items:
        cycle = cycles[name] = iterdict(items)
    return cycle['iter'].next()

#def counter(*args, **kwargs):
#    """Return the next cardinal in a sequence.
#
#    Every time ``counter`` is called, the value returned will be the next
#    counting number in that sequence.  This is reset to ``start`` on every
#    request, but can also be reset by calling ``reset_counter()``.
#
#    You can optionally specify the number you want to start at by passing
#    in the ``start`` argument (defaults to 1).
#
#    You can also optionally specify the step size you want by passing in
#    the ``step`` argument (defaults to 1).
#
#    Sequences will increase monotonically by ``step`` each time it is
#    called, until the heat death of the universe or python explodes.
#
#    This can be used to count rows in a table::
#
#        # In Myghty
#        % for item in items:
#        <tr>
#            <td><% h.counter() %></td>
#        </tr>
#        % #endfor
#
#    You can used named counters to prevent clashes in nested loops.
#    You'll have to reset the inner cycle manually though.  See the
#    documentation for ``webhelpers.text.cycle()`` for a similar
#    example.
#    """
#    # optional name of this list
#    name = kwargs.get('name', 'default')
#    # optional starting value for this sequence
#    start = kwargs.get('start', 1)
#    # optional step size of this sequence
#    step = kwargs.get('step', 1)
#
#    counters = request_config().environ.setdefault('railshelpers.counters', {})
#
#    # ripped off of itertools.count
#    def do_counter(start, step):
#        while True:
#            yield start
#            start += step
#
#    counter = counters.setdefault(name, do_counter(start, step))
#
#    return counter.next()
#
#def reset_counter(name='default'):
#    """Resets a counter.
#
#    Resets the counter so that it starts from the ``start`` cardinal in
#    the sequence next time it is used.
#    """
#    del request_config().environ['railshelpers.counters'][name]
#

def webmaster_email(text=None):
    """ E-mail link for the conference contact.

    Renders a link to the committee; optionally takes a text, which will be
    the text of the anchor (defaults to the e-mail address).
    """
    email = lca_info['webmaster_email']
    if text == None:
      text = email
    return link_to(text, 'mailto:' + email)

def contact_email(text=None):
    """ E-mail link for the conference contact.

    Renders a link to the committee; optionally takes a text, which will be
    the text of the anchor (defaults to the e-mail address).
    """
    email = lca_info['contact_email']
    if text == None:
        text = email

    return link_to(text, 'mailto:' + email)

def host_name():
    """ Name of the site (hostname)

    Returns the fqdn for the website.
    """
    return lca_info['event_host']

def event_name():
    """ Name of the event

    Returns the name of the event we're running (yay).
    """
    return lca_info['event_name']

def event_shortname():
    """

    Returns the short name of teh event we're running.
    """
    return lca_info['event_shortname']

#def get_temperature():
#    """ Fetch temperature from the BOM website.
#
#    This *REALLY* need to implement some sort of caching mechanism. Sadly I know no
#    python, so someone else is going to have to write it.
#    """
#    return urllib.urlopen('http://test.mel8ourne.org/dyn/temp.php').read()
#
#def array_random(a):
#    """Randomize the array
#    """
#    b = []
#    while len( a ) > 0:
#        j = random.randint(0, len( a ) - 1)
#        b.append( a.pop( j ) )
#    return b
#
#def random_pic(subdir):
#    """Mel8ourne random pic code.
#    """
#    fileprefix = '/srv/zookeepr/zookeepr/public/random-pix/'
#    htmlprefix = '/random-pix/'
#    try:
#        file = os.path.basename(random.choice(glob(fileprefix + subdir + '/*')))
#        return htmlprefix+subdir+'/'+file
#    except IndexError:
#        return "no images found"
#

def slideshow(set, small=None):
    """
    Generate a slideshow of a set of images, randomly selecting one to
    show first, unless a file is specified.
    """
    try:
        if small == None or small == "":
            # Randomly select a smaller image, set the width of the div to be
            # the width of image.
            small = random.choice(glob(file_paths["public_path"] + "/images/" + set + "/small/*"))
        else:
            small = file_paths["public_path"] + "/images/" + set + "/small/" + small

        output = "<div class=\"slideshow\" id=\"%s\" style=\"width: %dpx\">" % (set, int(Image.open(small).size[0]))
        small = os.path.basename(small)

        # Optionally load up some captions for the images.
        caption = dict()
        caption_file = file_paths['public_path'] + "/images/" + set + "/captions"
        if os.path.exists(caption_file):
          file = open(caption_file, 'r')
          captions = file.readlines()

          # Assign captions to a lookup table
          for cap in captions:
             str = cap.partition(':')
             caption[str[0]] = str[2]
    
        # Load up all the images in the set directory.
        files = glob(file_paths['public_path'] + "/images/" + set + '/*')
        for file in files:
            if os.path.isfile(file):
                short_file = os.path.basename(file)
                if file == 'captions':
                    continue

                output += "<a href=\"" + file_paths["public_html"] + "/images/" + set + "/" + short_file + "\" rel=\"lightbox[" + set + "]\""
                if short_file in caption:
                    output += " title=\"" + caption[short_file] + "\""
                output += ">"

                # If we're looking at the small one we've picked, display
                # it as well.
                if short_file == small:
                    output += "<img src=\"" +  file_paths["public_html"] + "/images/" + set + "/small/" + short_file + "\">"
    
                    # If there are more than one image in the slideshow
                    # then also display "more...".
                    if files.__len__() > 1:
                       output += '<div class="more">More images...</div>'
                output += "</a>\n";
        output += "</div>\n"
        return output
               
    except IndexError:
        return "no images found"


break_re = re.compile(r'(\n|\r\n)(?!\s*<(li|ul|ol)>)')
def line_break(s):
    """ Turn line breaks into <br>'s """
    return break_re.sub('<br />', s)

def yesno(bool):
    """ Display a read-only checkbox for the value provided """
    if bool:
        return '&#9745;'
    else:
        return '&#9744;'

#def num(x):
#    """ Display a number or none if a number wasn't entered """
#    if x==None:
#        return 'none'
#    else:
#        return x
#
def date(d):
    """ Display a date in text format (currently limited to the month that is hardcoded) """
    if d==1:
        return "%dst of January" % d
    elif d==2:
        return "%dnd of January" % d
    elif d==3:
        return "%drd of January" % d
    elif d<15:
        return "%dth of January" % d
    elif d==31:
        return "%dst of January" % d
    else:
        return "%dth of January" % d

def countries():
    """ list of countries
    """

    # FIXME we should probably store the country codes rather than the country names
    # http://pylonshq.com/docs/en/0.9.7/thirdparty/webhelpers/constants/
    lines = webhelpers.constants.country_codes()
    res = []
    for line in lines:
        country = line[1]
        res.append(country)
    res.sort()
    return res

def debug():
    return config['pylons.errorware']['debug']

teaser_re = re.compile(r'(\<\!\-\-break\-\-\>)')
def make_teaser(body):
    if teaser_re.search(body):
        parts = teaser_re.split(body)
        return parts[0], True
    else:
        return body, False

def remove_teaser_break(body):
    if teaser_re.search(body):
        return teaser_re.sub('', body)
    else:
        return body

computer_re = re.compile(r'([^A-Za-z0-9\_\-])')
def computer_title(title):
    """ Turn a string into a computer friendly tag """
    title = title.replace(' ', '_')
    title = computer_re.sub('', title)
    title = title.lower()
    return title

def wiki_link(title):
    """ Turn a string into a wiki friendly tag """
    parts = title.split(' ')
    title = ''.join([part.title() for part in parts])
    title = computer_re.sub('', title)
    return title

def featured_image(title, big = False):
    """
    Returns img src If an image exists in /public/featured/ with the same
    computer-friendly title as a news item it becomes featured down the left If
    big == True then find a directory
    """

    fileprefix = file_paths['news_fileprefix']
    htmlprefix = file_paths['news_htmlprefix']

    if big:
        # look for folder feature
        if os.path.isdir(fileprefix + "/" + computer_title(title)):
            return htmlprefix + "/" + computer_title(title) + "/"
        else:
            return False
    else:
        # look for image
        if os.path.isfile(fileprefix + "/" + computer_title(title) + ".png"):
            return htmlprefix + "/" + computer_title(title) + ".png"
        else:
            return False

    return False

domain_re = re.compile('^(http:\/\/|ftp:\/\/)?(([a-z]+[a-z0-9]*[\.|\-]?[a-z]+[a-z0-9]*[a-z0-9]+){1,4}\.[a-z]{2,4})')
def domain_only(url):
    """ Truncates a url to the domain only. For use with "in the press" """
    match = domain_re.match(url)
    if match:
        return match.group(2)
    else:
        return url

def extension(name):
    """ Return the extension of a file name"""
    return name.split('.')[-1]

def silly_description():
    adverb = random.choice(lca_rego['silly_description']['adverbs'])
    adjective = random.choice(lca_rego['silly_description']['adjectives'])
    noun = random.choice(lca_rego['silly_description']['nouns'])
    start = random.choice(lca_rego['silly_description']['starts'])
    if start == 'a' and adverb[0] in ['a', 'e', 'i', 'o', 'u']:
        start = 'an'
    desc = '%s %s %s %s' % (start, adverb, adjective, noun)
    descChecksum = silly_description_checksum(desc)
    return desc, descChecksum

def silly_description_checksum(desc):
    import hashlib
    salted = desc + unicode('Use the source Luke')
    return hashlib.sha1(salted.encode('latin1')).hexdigest()

#def ticket_percentage_text(percent, earlybird = False):
#    if percent == 100:
#        return 'All tickets gone.'
#    elif percent >= 97.5:
#        if earlybird:
#            return "Earlybird almost soldout."
#        else:
#            return "Almost all tickets gone."
#    else:
#        if earlybird:
#            return "%d%% earlybird sold." % percent
#        else:
#            return "%d%% tickets sold." % percent

link_re = re.compile(r'\[url\=((http:\/\/|ftp:\/\/)?(([a-z]+[a-z0-9]*[\.|\-]?[a-z]+[a-z0-9]*[a-z0-9]+){1,4}\.[a-z]{2,4})([^ \t\n]+))\](.*)\[\/url\]')
def url_to_link(body):
    """ Converts [url=http://example.com]site[/url] into <a href="http://www.example.com">site</a>> """
    return link_re.sub(r'<a href="\1" title="\1">\6</a>', body)

def signed_in_person():
    email_address = request.environ.get("REMOTE_USER")
    if email_address is None:
        return None

    person = Person.find_by_email(email_address, True)
    return person

def object_to_defaults(object, prefix):
    defaults = {}

    for key in object_mapper(object).columns.keys():
        value = getattr(object, key)
        if type(value) == list:
            for code in value:
                defaults['.'.join((prefix,key,code))] = 1
            defaults['.'.join((prefix,key))] = ','.join(value)
        elif value == True:
            defaults['.'.join((prefix,key))] = 1
        else:
            defaults['.'.join((prefix,key))] = value

    return defaults

def check_flash():
    # If the session data isn't of the particular format python has trouble.
    # So we check that it is a dict.
    if session.has_key('flash'):
        if type(session['flash']) != dict:
            del session['flash']
            session.save()

def get_flashes():
    check_flash()
    if not session.has_key('flash'):
        return None
    messages = session['flash']
    # it is save to delete now
    del(session['flash'])
    session.save()
    return messages

def flash(msg, category="information"):
    check_flash()
    if not session.has_key('flash'):
        session['flash'] = {}
    if not session['flash'].has_key(category):
        session['flash'][category] = []
    session['flash'][category].append(msg)
    session.save()

def zk_root():
    """ Helper function to return the root directory of zookeepr,
    this allows completely relevant URL's """
    pass #TODO

def number_to_currency(number, unit='$', precision=2):
    # TODO: use commas to separate thousands
    return unit + "%#.*f" % (precision, number)

def number_to_percentage(number):
    return str(number) + '%'

def sales_tax(amount):
    """ Calculate the sales tax that for the supplied amount. """
    if 'sales_tax_multiplier' in lca_info:
      sales_tax = int(amount * lca_info['sales_tax_multiplier'])
    elif 'sales_tax_divisor' in lca_info:
      sales_tax = int(amount / lca_info['sales_tax_divisor'])
    else:
      # wtf?
      sales_tax = 0

    return sales_tax

def latex_clean(str):
    """ Sanitise a string suitable for use in LaTeX. """
    str = str.replace('_', '\_')
    str = str.replace('<', '$<$')
    str = str.replace('>', '$>$')
    str = str.replace('&lt;', '$<$')
    str = str.replace('&gt;', '$>$')
    str = str.replace('&', '\&')
    str = str.replace('C#', 'C\#')
    str = re.sub('"(.*?)"', "``\\1''", str)
    str = re.sub('<b>(.*?)</b>', '\\\\textbf{\\1}', str)
    str = re.sub('<i>(.*?)</i>', "\emph{\\1}", str)
    str = re.sub('<ol(.*?)>', '\\\\begin{enumerate}\n', str)
    str = str.replace('</ol>', '\end{enumerate}\n')
    str = str.replace('<ul>', '\\begin{itemize}\n')
    str = str.replace('</ul>', '\end{itemize}\n')
    str = str.replace('<li>', '\item ')
    str = str.replace('</li>', '')
    str = str.replace('<pre>', '\\begin{verbatim}')
    str = str.replace('</pre>', '\end{verbatim}')
    str = str.replace('$', '\$')
    str = str.replace('<div>', '')
    str = str.replace('</div>', '')
    str = str.replace('<p>', '')
    str = str.replace('</p>', '')

    return str

def html_clean(str):
    """ Clean up HTML to be safe """
    cleaner = Cleaner(safe_attrs_only=True)
    return cleaner.clean_html(str)
    
    
    
def url_for(*args, **kwargs):
    fields = dict(request.GET)
    extra = ''
    if fields.has_key('hash'):
        extra='?hash=' + fields['hash']
    return pylons_url_for(*args, **kwargs) + extra

def list_to_string(list, primary_join='%s and %s', secondary_join=', ', html = False):
    if html:
        list = [escape(item) for item in list]
    if len(list) == 0:
        list = ''
    elif len(list) == 1:
        list = list[0]
    else:
        list = primary_join % (secondary_join.join(list[: -1]), list[-1])
    return list
