# encoding: utf-8

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
	if entry.comments.filter(notification=True, author=user).count() == 1:
		return False
	else:
		return True

@register.simple_tag
def show_warning():
	return COMMENTS_WARNING

@register.inclusion_tag('blog/latest_comments.html')
def get_latest_comments():
	return {
		"latest_comments": Comments.objects.all()[:settings.LATEST_COMMENTS_LIMIT]
	}