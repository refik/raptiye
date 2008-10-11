#-*- encoding: utf8 -*-
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

register = template.Library()

@register.tag
def poll(parser, token):
	from raptiye.polls.models import Poll
	
	if Poll.objects.filter(published=True).count():
		return PollNode(Poll.objects.filter(published=True).latest())
	else:
		return PollNode(None)

class PollNode(template.Node):
	def __init__(self, poll):
		self.poll = poll

	def render(self, context):
		context["poll"] = self.poll
		return ""