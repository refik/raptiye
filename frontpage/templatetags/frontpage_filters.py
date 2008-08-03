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
	tag_name, lang = token.split_contents()
	
	fp = None
	
	if FrontPage.objects.filter(language=lang).count() == 1:
		fp = FrontPage.objects.get(language=lang)
	else:
		fp = FrontPage.objects.get(language='tr')
	
	return MainPageNode(fp)

class MainPageNode(template.Node):
	def __init__(self, fp):
		self.fp = fp
	
	def render(self, context):
		context['mainpage'] = self.fp
		return ""

@register.filter
def language_trim(value):
	'Removes the leading language part of the URL'
	leading_codes = '/'
	for lang in settings.LANGUAGES:
		leading_codes += lang[0]
	return value.lstrip(leading_codes)