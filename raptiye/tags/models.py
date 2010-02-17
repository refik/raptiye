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

from django.db import models
from django.utils.translation import ugettext_lazy as _

from raptiye.blog.models import Entry

class Tag(models.Model):
    """
    Common class to use with other models

    """

    name = models.CharField(_(u"Tag Name"), max_length=30, unique=True)
    slug = models.SlugField(_(u"URL"), max_length=50)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _(u"Tag")
        verbose_name_plural = _(u"Tags")
        ordering = ["name"]

class TaggedEntry(Entry):
    tags = models.ManyToManyField(Tag, verbose_name=_(u"Tags"), related_name="entries")
    
    class Meta:
        app_label = "blog"
        verbose_name = _(u"Entry")
        verbose_name_plural = _(u"Entries")
