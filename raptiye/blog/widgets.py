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

import json

from django import forms
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from tagging.models import Tag

from raptiye.blog.models import Entry

__all__ = ("MarkItUpInput", "AutoCompleteTagInput")

class MarkItUpInput(forms.Textarea):
    def __init__(self, *args, **kwargs):
        super(MarkItUpInput, self).__init__(*args, **kwargs)

    class Media:
        css = {
            "screen": (
                "css/markitup/skins/default/style.css",
                "css/markitup/sets/default/style.css",
            )
        }

        js = (
            "js/markitup/jquery.markitup.pack.js",
            "js/markitup/sets/default/set.js",
        )

    def render(self, name, value, attrs=None):
        output = super(MarkItUpInput, self).render(name, value, attrs)
        return output + mark_safe(u'''<script type="text/javascript" charset="utf-8">
            $("#id_%s").markItUp(mySettings)
        </script>''' % name)

class AutoCompleteTagInput(forms.TextInput):
    def __init__(self, *args, **kwargs):
        if kwargs.has_key("model"):
            self.model = kwargs.get("model", Entry)
            del(kwargs["model"])

        super(AutoCompleteTagInput, self).__init__(*args, **kwargs)
        self.startText = _(u"Enter Tag Name Here")
        self.emptyText = _(u"No Results")

    class Media:
        css = {
            "screen": ("css/autoSuggest.css",)
        }

        js = (
            "js/jquery.autoSuggest-packed.js",
        )

    def render(self, name, value, attrs=None):
        output = super(AutoCompleteTagInput, self).render(name, value, attrs)
        tags = Tag.objects.usage_for_model(self.model)
        tag_list = json.dumps([{"name": t.name, "value": t.name} for t in tags])
        value = (",".join(value.split(" ")) if value.find(",") == -1 else value) if value else ""
        return output + mark_safe(u'''<script type="text/javascript" charset="utf-8">
            $("#id_%s").autoSuggest(%s, {
                "asHtmlID": "%s",
                "preFill": "%s",
                "startText": "%s",
                "emptyText": "%s",
                "neverSubmit": true
            })
            
            $("form").submit(function() {
                $("<input>").attr({
                    "name": "%s",
                    "type": "hidden"
                }).val(
                    $("#as-values-%s").val()
                ).appendTo($("form"))
            })
        </script>''' % (name, tag_list, name, value, self.startText, self.emptyText, name, name))
