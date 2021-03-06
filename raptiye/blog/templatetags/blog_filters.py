# coding: utf-8
# 
# raptiye
# Copyright (C) 2009  Alper KANAT <alperkanat@raptiye.org>
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
# 

from datetime import date
import HTMLParser
import re

from django import template
from django.conf import settings
from django.contrib.sites.models import Site
from django.utils.safestring import mark_safe

from raptiye.blog.models import Entry, Link
from raptiye.blog.webcal import WebCalendar

register = template.Library()

@register.simple_tag
def calculate_age():
    return (date.today() - settings.BIRTH_DATE).days/365

@register.simple_tag
def construct_calendar():
    today = date.today()
    wc = WebCalendar(today.year, today.month, today.day, Entry.objects, "datetime", settings.LOCALES['tr'])
    return wc.render("calendar_table", "/blog", "ulink")

@register.inclusion_tag('pagination.html', takes_context=True)
def paginator(context, adjacent_pages=2):
    """
    To be used in conjunction with the object_list generic view.

    Adds pagination context variables for use in displaying first, adjacent and
    last page links in addition to those created by the object_list generic
    view.

    """

    page_numbers = range(max(1, context['page'] - adjacent_pages), min(context['pages'], context['page'] + adjacent_pages) + 1)

    params = context["request"].GET.copy()

    if params.__contains__("page"):
        del(params["page"])

    return {
        'page': context['page'],
        'pages': context['pages'],
        'page_numbers': page_numbers,
        'next': context['next'],
        'previous': context['previous'],
        'has_next': context['has_next'],
        'has_previous': context['has_previous'],
        'show_first': 1 not in page_numbers,
        'show_last': context['pages'] not in page_numbers,
        'query_string': params.urlencode(),
    }

@register.inclusion_tag('links.html')
def links():
    return {'links': Link.objects.all()}

@register.filter
def emotions(entry):
    if settings.ENABLE_EMOTIONS:
        return entry

    site = Site.objects.get_current()

    icons = {
        ":)": "%simages/smiley/face-smile.png" % settings.MEDIA_URL,
        ":|": "%simages/smiley/face-plain.png" % settings.MEDIA_URL,
        ":(": "%simages/smiley/face-sad.png" % settings.MEDIA_URL,
        ":D": "%simages/smiley/face-grin.png" % settings.MEDIA_URL,
        ";-)": "%simages/smiley/face-wink.png" % settings.MEDIA_URL,
    }

    for smiley, src in icons.iteritems():
        entry = entry.replace(smiley, " <img src='%s' align='absmiddle'> " % (site.domain, src))

    return entry

@register.inclusion_tag("twitter.html")
def twitter():
    """
    Gets the latest Twitter status updates of the blog author
    using the credentials in settings.py

    """

    if settings.ENABLE_TWITTER_BOX:
        try:
            import twitter
            api = twitter.Api(username=settings.TWITTER_USERNAME, password=settings.TWITTER_PASSWORD)
            latest_updates_of_user = [status.GetText() for status in api.GetUserTimeline()]
            return {"latest_updates": latest_updates_of_user[:settings.TWITTER_LIMIT]}
        except:
            pass

    return {"latest_updates": None}

@register.filter
def twitter_specials(tweet):
    isReply = lambda s: s.startswith("@")
    isHashTag = lambda s: s.startswith("#")
    specials = re.findall("@[^\s]+|#[^\s]+", tweet)
    unique_specials = set(specials)

    for tag in unique_specials:
        linked_tag = tag

        if isReply(tag):
            linked_tag = '<a href="http://twitter.com/%s/" target="_blank">%s</a>' % (tag.replace("@", ""), tag)
        elif isHashTag(tag):
            linked_tag = '<a href="http://twitter.com/search?q=%s" target="_blank">%s</a>' % (tag, tag)

        tweet = tweet.replace(tag, linked_tag)

    return mark_safe(tweet)

@register.filter
def exceeds_limit(entry):
    if len(entry.split()) > 150:
        return True
    return False

@register.filter
def code_colorizer(entry):
    """
    Uses BeautifulSoup to find and parse the code in the entry 
    that will be colorized and changes it according to the syntax 
    specs using pygments.

    The HTML code should include the colorized code wrapped into a 
    div which has language (e.g. python) as id and "code" as class 
    attributes.

    Best part of using a filter is that we don't have to change the 
    real post containing the code. The worst part is that we have to 
    search for the code layer in each post.

    """

    if settings.COLORIZE_CODE:
        try:
            from BeautifulSoup import BeautifulSoup, Tag
            from pygments import highlight
            from pygments.lexers import get_lexer_by_name
            from pygments.formatters import HtmlFormatter
        except ImportError:
            return entry

        try:
            parser = BeautifulSoup(entry, convertEntities=BeautifulSoup.ALL_ENTITIES)
        except HTMLParser.HTMLParseError:
            return entry

        # searching for code blocks in the blog entry
        code_blocks = parser.findAll("div", attrs={"class": "code"})

        if len(code_blocks) > 0:
            for block in code_blocks:
                # if the code block's wrapper div doesn't have an id
                # attribute don't colorize the code
                if block.attrMap.has_key("id"):
                    language = block.attrMap["id"]
                else:
                    continue

                # finding the exact place of the code
                layer = block.div if block.div else block
                # removing any html tags inside the code block
                [tag.extract() for tag in layer.findAll()]
                # getting the original code in the block
                code = "".join(layer.contents)
                # colorizing the code
                lexer = get_lexer_by_name(language)
                formatter = HtmlFormatter(linenos="table", style="tango", cssclass="code")
                colorized_code = Tag(parser, "div") if block.div else Tag(parser, "div", attrs=(("id", language), ("class", "code")))
                colorized_code.insert(0, highlight(code, lexer, formatter))
                layer.replaceWith(colorized_code)

            return parser.renderContents()

    return entry

@register.simple_tag
def project_name():
    return settings.PROJECT_NAME

@register.simple_tag
def version():
    return settings.VERSION

@register.simple_tag
def project_subtitle():
    return settings.PROJECT_SUBTITLE

@register.simple_tag
def rss_url():
    return settings.RSS_URL
