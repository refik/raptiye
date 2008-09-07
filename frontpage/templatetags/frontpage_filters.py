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