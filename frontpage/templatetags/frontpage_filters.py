# raptiye
# Copyright (C)  Alper KANAT  <alperkanat@raptiye.org>
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
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from django import template
from django.conf import settings
from raptiye.frontpage.models import FrontPage

register = template.Library()

@register.filter
def order_by(value, arg):
	"Orders the result by given argument"
	return value.order_by(arg).exclude(level=0)

@register.tag
def get_mainpage(parser, token):
	fp = FrontPage.objects.get(pk=1)
	return MainPageNode(fp)

class MainPageNode(template.Node):
	def __init__(self, fp):
		self.fp = fp
	
	def render(self, context):
		context['mainpage'] = self.fp
		return ""

@register.filter
def replace_with_version(value):
	return value.replace("[[VERSION]]", settings.VERSION)