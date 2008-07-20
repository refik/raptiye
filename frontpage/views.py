#-*- encoding: utf-8 -*-

from django.shortcuts import render_to_response
from django.template import RequestContext
from raptiye.blog.views import get_latest_entries_list

def index(request, template_name='frontpage/homepage.html'):
	# getting latest blog entries (with limit in settings)
	entries = get_latest_entries_list()
	# put them together into a dict
	dict = {
		'entries': entries
	}
	# now we have everything.. let's show it..
	return render_to_response(template_name, dict, context_instance=RequestContext(request))
