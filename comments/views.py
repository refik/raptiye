#-*- encoding: utf-8 -*-
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

from datetime import datetime
from os import path
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.sites.models import Site
from django.core.mail import mail_admins
from django.http import HttpResponse
from django.utils import simplejson
from raptiye.blog.models import Entry
from raptiye.comments.models import Comments
from raptiye.extra.captcha import Captcha
from raptiye.extra import messages

def new_captcha(request):
	resp = {
		"status": 0,
	}
	# set session variable to avoid attacks
	# when the user exceeds 10 captcha's limit 
	# it has to wait 10 minutes
	now = datetime.now()
	if request.session.__contains__("captcha_counter") and request.session.__contains__("captcha_datetime"):
		if request.session["captcha_counter"] == settings.CAPTCHA_RENEWAL_LIMIT:
			if (now - request.session["captcha_datetime"]).seconds/60 > settings.CAPTCHA_PENALTY:
				# resetting datetime of captcha
				request.session["captcha_datetime"] = datetime.now()
			else:
				resp["status"] = 1
				resp["error"] = messages.OPERATION_FAILURE
				return HttpResponse(simplejson.dumps(resp))
		request.session["captcha_counter"] += 1
		request.session["captcha_datetime"] = datetime.now()
	else:
		request.session["captcha_counter"] = 1
		request.session["captcha_datetime"] = datetime.now()
	# create a new captcha and send back its url
	captcha = create_captcha()
	resp["captcha"] = captcha
	return HttpResponse(simplejson.dumps(resp))

def comment_sent(request):
	# FIXME: remove hardcoded strings
	
	from raptiye.comments.forms import CommentForm
	from raptiye.extra.mail import send_comment_notification
	
	resp = {
		"status": 0,
	}
	
	site = Site.objects.get_current()
	
	# checking if the user is authenticated
	if request.user.is_authenticated() or settings.ALLOW_ANONYMOUS_COMMENTS:
		# checking POST data
		test = lambda x={},y="": (x.has_key(y) and x[y] != "") or False
		if test(request.POST, "entry_id") and test(request.POST, "captcha_id") and test(request.POST, "comment_body") and test(request.POST, "captcha"):
			# FIXME: change the following part in the future..
			if not request.user.is_authenticated() and settings.ALLOW_ANONYMOUS_COMMENTS:
				# if anonymous user can comment then validate the form
				form = CommentForm(request.POST)
				if not form.is_valid():
					resp["status"] = 1
					# transforming errors into a form suitable for comments page
					errors = []
					for error in form.errors:
						errors.append(messages.INVALID_FORM_FIELD % form.fields[error].label)
					resp["error"] = errors
					# returning the response
					return HttpResponse(simplejson.dumps(resp))
			
			# and at last, checking captcha
			cp = Captcha()
			cp.text = request.POST["captcha"]
			if cp.generate_hash(settings.SECRET_KEY[:20]) == request.POST["captcha_id"]:
				# all tests ok, creating comment
				c = Comments()
				c.entry = Entry.objects.get(id=request.POST["entry_id"])
				# getting the user who makes the comment
				if request.user.is_authenticated():
					user = request.user
				else:
					user = User.objects.get(username="anonymous")
					# checking anonymous post data
					if settings.ALLOW_ANONYMOUS_COMMENTS and test(request.POST, "anonymous_email") and test(request.POST, "anonymous_full_name"):
						# filling anonymous user information from post data
						c.anonymous_author = request.POST["anonymous_full_name"]
						c.anonymous_author_email = request.POST["anonymous_email"]
						if test(request.POST, "anonymous_website"):
							c.anonymous_author_web_site = request.POST["anonymous_website"]
					else:
							resp["status"] = 1
							resp["error"] = messages.MISSING_INFORMATION
							return HttpResponse(simplejson.dumps(resp))
				c.author = user
				c.content = request.POST["comment_body"]
				c.datetime = datetime.now()
				# checking if the user has a published comment before
				if request.user.is_authenticated() and user.comments.filter(published=True).count() > 0:
					c.published = True
				else:
					# send notification to the admins
					mail_admins(messages.NEW_COMMENT_SUBJECT, 
						messages.NEW_COMMENT_BODY % (c.entry, "http://%s/admin/blog/entry/%s/" % (site.domain, c.entry.id)), 
						fail_silently=True)
				# if notification is true
				if test(request.POST, "notification") and not user_has_notification(request):
					c.notification = True
				# saving comment
				c.save()
				# now let's mail the people who wants a notification for this entry
				# iff the comment is published
				if c.published:
					send_comment_notification(c.entry, user)
				resp["success"] = messages.COMMENT_SENT
				return HttpResponse(simplejson.dumps(resp))
			else:
				resp["status"] = 1
				resp["error"] = messages.CAPTCHA_FAILURE
				return HttpResponse(simplejson.dumps(resp))
		else:
			resp["status"] = 1
			resp["error"] = messages.OPERATION_FAILURE
			return HttpResponse(simplejson.dumps(resp))
	else:
		# if the user is anonymous
		resp["status"] = 1
		resp["error"] = messages.LOGIN_NEEDED
		return HttpResponse(simplejson.dumps(resp))

# above method will require login if a variable is True in the settings.py
if not settings.ALLOW_ANONYMOUS_COMMENTS:
	comment_sent = login_required(comment_sent)

def create_captcha():
	from random import choice
	
	fonts = {
		"butterunsalted.ttf": 32,
		"astonish.ttf": 40,
		"elecha.ttf": 25,
		"times.ttf": 25
	}
	
	c = Captcha(file_path=path.join(settings.MEDIA_ROOT, settings.TEMP_MEDIA_PREFIX), size=(120, 50))
	c.filename = c.generate_hash(settings.SECRET_KEY[:20]) + ".jpg"
	# selecting the font randomly
	font = choice(fonts.keys())
	c.set_font(path.join(settings.MEDIA_ROOT, "fonts", font), fonts[font])
	c.generate_captcha()
	return path.join("/media/", settings.TEMP_MEDIA_PREFIX, c.filename)

def user_has_notification(request):
	"""
	Checks if the user has previously submitted a comment with the 
	notification flag..
	
	This method assumes that the POST variables are already set and
	controlled.
	"""
	# getting entry
	entry = Entry.objects.get(id=request.POST["entry_id"])
	
	if request.user.is_authenticated():
		email = request.user.email
		if entry.comments.filter(notification=True, author__email=email).count() > 0:
			return True
	else:
		email = request.POST["anonymous_email"]
		if entry.comments.filter(notification=True, anonymous_author_email=email).count() > 0:
			return True
	
	return False