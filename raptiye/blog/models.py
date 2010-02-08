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

from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _

class Entry(models.Model):
    """
    Entry Class

    This is the class we hold every post for the blog. It
    can be either in Turkish or English due to the choices
    in settings.

    """

    title = models.CharField(_(u"Title"), help_text=_(u"Required"), max_length=80)
    datetime = models.DateTimeField(_(u"Publish On"), help_text=_(u"Required"))
    content = models.TextField(_(u"Content"), help_text=_(u"Required.. HTML Allowed.."))
    sticky = models.BooleanField(_(u"Sticky"), default=False)
    language = models.CharField(_(u"Language"), choices=settings.LANGUAGES, default="tr", max_length=2)
    published = models.BooleanField(_(u"Published"), default=False)
    comments_enabled = models.BooleanField(_(u"Comments Enabled"), default=True)
    slug = models.SlugField(_(u"URL"), max_length=100)

    def __unicode__(self):
        return self.title

    class Meta:
        get_latest_by = "datetime"
        ordering = ["-datetime", "title", "content"]
        verbose_name = _(u"Entry")
        verbose_name_plural = _(u"Entries")

class Link(models.Model):
    'The model that stores the links to outer web sites..'

    title = models.CharField(_(u"Title"), max_length="50")
    description = models.CharField(_(u"Description"), max_length="200", blank=True)
    url = models.URLField(_(u"URL"))
    window = models.BooleanField(_(u"Open in new window"), default=False)

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _(u"Link")
        verbose_name_plural = _(u"Links")
        ordering = ["title",]

