#-*- encoding: utf8 -*-

from django import template

register = template.Library()

@register.inclusion_tag('blog/poll.html')
def poll():
	'Adds all link categories and their links to the context..'
	
	from raptiye.polls.models import Poll
	
	return {
		'poll': Poll.objects.latest(),
	}