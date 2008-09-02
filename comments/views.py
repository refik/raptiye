#-*- encoding: utf-8 -*-

from datetime import datetime
from os import path
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils import simplejson
from raptiye.blog.models import Entry
from raptiye.comments.models import Comments
from raptiye.extra.captcha import Captcha
from raptiye.extra.messages import *

resp = {
	"status": 0,
}

def new_captcha(request):
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
				resp["error"] = u"işlem başarısız.."
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

@login_required
def comment_sent(request):
	from raptiye.extra.mail import send_comment_notification
	
	# checking if the user is authenticated
	if request.user.is_authenticated():
		# checking POST data
		test = lambda x={},y="": (x.has_key(y) and x[y] != "") or False
		if test(request.POST, "entry_id") and test(request.POST, "captcha_id") and test(request.POST, "comment_body") and test(request.POST, "comment_captcha"):
			# and at last, checking captcha
			cp = Captcha()
			cp.set_text(request.POST["comment_captcha"])
			if cp.generate_hash(settings.SECRET_KEY[:20]) == request.POST["captcha_id"]:
				# all tests ok, creating comment
				c = Comments()
				c.entry = Entry.objects.get(id=request.POST["entry_id"])
				c.author = request.user
				c.content = request.POST["comment_body"]
				c.datetime = datetime.now()
				# checking if the user has a published comment before
				if request.user.comments.filter(published=True).count() > 0:
					c.published = True
				# if notification is true
				if test(request.POST, "notification"):
					c.notification = True
				# saving comment
				c.save()
				# now let's mail the people who wants a notification for this entry
				send_comment_notification(c.entry)
				resp["success"] = u"yorumunuz gönderildi.."
				return HttpResponse(simplejson.dumps(resp))
			else:
				resp["error"] = u"captcha hatalı"
				return HttpResponse(simplejson.dumps(resp))
		else:
			resp["error"] = u"işlem başarısız"
			return HttpResponse(simplejson.dumps(resp))
	else:
		# if the user is anonymous
		resp["error"] = u"giriş yapılmamış"
		return HttpResponse(simplejson.dumps(resp))

def create_captcha():
	c = Captcha(path.join(settings.MEDIA_ROOT, settings.TEMP_MEDIA_PREFIX))
	text = c.generate_random_text()
	c.set_text(text)
	# setting filename to the hash of text
	c.set_filename(c.generate_hash(settings.SECRET_KEY[:20]) + ".jpg")
	c.set_size(120, 50)
	c.set_fg_color("black")
	c.set_bg_color("white")
	c.set_font(path.join(settings.MEDIA_ROOT, "fonts", "astonish.ttf"), 40)
	c.generate_captcha()
	return path.join("/media/", settings.TEMP_MEDIA_PREFIX, c.get_filename())
