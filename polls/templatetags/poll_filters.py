#-*- encoding: utf8 -*-

from django import template

register = template.Library()

@register.tag
def poll(parser, token):
	from raptiye.polls.models import Poll
	
	if Poll.objects.count():
		return PollNode(Poll.objects.filter(published=True).latest())
	else:
		return PollNode(None)

class PollNode(template.Node):
	def __init__(self, poll):
		self.poll = poll

	def render(self, context):
		context["poll"] = self.poll
		return ""