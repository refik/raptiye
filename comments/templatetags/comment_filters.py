# encoding: utf-8
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
from raptiye.comments.models import Comments
from raptiye.extra.messages import COMMENTS_WARNING

register = template.Library()

@register.filter
def has_published_comment(user):
	if user.is_authenticated():
		if user.comments.filter(published=True).count() > 0:
			return 1
	return 0

@register.filter
def check_if_user_subscribed(entry, user):
	if user.is_authenticated():
		if entry.comments.filter(notification=True, author=user).count() == 1:
			return False
		else:
			return True
	else:
		return False

@register.simple_tag
def show_warning():
	return COMMENTS_WARNING

@register.inclusion_tag('blog/latest_comments.html')
def get_latest_comments():
	return {
		"latest_comments": Comments.objects.filter(published=True)[:settings.LATEST_COMMENTS_LIMIT]
	}