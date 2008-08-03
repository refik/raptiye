#-*- encoding: utf-8 -*-

from django.shortcuts import render_to_response
from django.template import RequestContext
from raptiye.blog.views import get_latest_entries_list

def index(request, lang='', template_name='frontpage/homepage.html'):
	dict = {
		'entries': get_latest_entries_list(lang),
	}
	if lang is '':
		return render_to_response(template_name, dict, context_instance=RequestContext(request))
	else:
		return render_to_response('frontpage/homepage_en.html', dict, context_instance=RequestContext(request))