#-*- encoding: utf-8 -*-

from contrib.session_messages import create_message
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from raptiye.blog.views import get_latest_entries
from raptiye.comments.models import Comments
from raptiye.comments.views import create_captcha
from raptiye.extra.captcha import Captcha
from raptiye.extra.filters import is_username_unique, is_email_unique
from raptiye.extra.gravatar import get_gravatar
from raptiye.extra.mail import *
from raptiye.extra.messages import *
from raptiye.users.forms import *

def gravatar(request, username):
	if request.method == "POST" and request.POST.has_key("email"):
		site = Site.objects.get(pk=1)
		email = request.POST["email"]
	return HttpResponse(get_gravatar(email, "http://" + site.domain + settings.DEFAULT_AVATAR))

def notification_remove(request, username):
	# will return json object if the operation is successfull
	from django.utils import simplejson

	if request.method == "GET" and request.GET.has_key("id"):
		id = request.GET["id"]
		try:
			comment = Comments.objects.get(id=id)
			comment.notification = False
			comment.save()
			user = User.objects.get(username=username)
			watched_comments = user.comments.order_by("-datetime").filter(notification=True)
			list = []
			for comment in watched_comments:
				list.append({"id": comment.id, "title": comment.entry.title, "url": comment.entry.get_url()})
			# returning json rep. of list
			return HttpResponse(simplejson.dumps(list))
		except:
			return HttpResponse("<resp><status>1</status></resp>")
	else:
		return HttpResponse("<resp><status>1</status></resp>")
	return HttpResponse("<resp><status>0</status></resp>")

def profile(request, username, template="users/profile.html"):
	if request.user.is_authenticated and request.user.username == username:
		# sometimes we need to log the user out
		logoutUser = False
		# getting the user information
		user = User.objects.get(username=username)
		profile = user.get_profile()

		if request.method == 'POST':
			form = ProfileForm(request.POST)
			extra_context = {
				"form" : form,
				"latest_comments": user.comments.order_by("-datetime")[:5],
				"watched_comments": user.comments.order_by("-datetime").filter(notification=True)[:5],
			}
			if form.is_valid():
				if form.cleaned_data["password"] != user.password[:10]:
					user.set_password(form.cleaned_data["password"])
					logoutUser = True
				user.first_name = form.cleaned_data["name"]
				user.last_name = form.cleaned_data["surname"]
				if form.cleaned_data["email"] != user.email:
					user.email = form.cleaned_data["email"]
					# turning on activation for user
					user.is_active = False
					profile.activation_key = create_activation_key()
					# mailing user for activation
					site = Site.objects.get(pk=1)
					send_mail(ACTIVATION_SUBJECT, 
							ACTIVATION_BODY % (site.name, site.domain, user.username, profile.activation_key), 
							settings.EMAIL_INFO_ADDRESS_TR, [user.email,], 
							fail_silently=settings.EMAIL_FAIL_SILENCE,
							auth_user=settings.EMAIL_HOST_USER, 
							auth_password=settings.EMAIL_HOST_PASSWORD)
					logoutUser = True
				# getting profile of user
				if form.cleaned_data["avatar"] != "":
					profile.avatar = form.cleaned_data["avatar"]
				profile.web_site = form.cleaned_data["website"]
				# saving user and his profile
				user.save()
				profile.save()
				if logoutUser:
					logout(request)
				# leaving message to the user
				user.message_set.create(message=PROFILE_SUCCESS)
				# redirecting back to the profile page
				return HttpResponseRedirect(reverse("profile_page", args=[user.username]))
			else:
				return render_to_response(template, extra_context, context_instance=RequestContext(request))
		else:
			form = ProfileForm(initial={
					"username": user.username,
					"password": user.password[:10],
					"name": user.first_name,
					"surname": user.last_name,
					"email": user.email,
					"avatar": "" if user.get_profile().avatar == settings.DEFAULT_AVATAR else user.get_profile().avatar,
					"website": user.get_profile().web_site,
				},
				auto_id=True)
			extra_context = {
				"form" : form,
				"latest_comments": user.comments.order_by("-datetime")[:5],
				"watched_comments": user.comments.order_by("-datetime").filter(notification=True)[:5],
			}
		return render_to_response(template, extra_context, context_instance=RequestContext(request))
	else:
		return get_latest_entries(request, PROFILE_ACCOUNT_ERROR)

def activation(request, username, key):
	from datetime import datetime
	
	if User.objects.filter(username=username).count() == 1:
		user = User.objects.get(username=username)
		if user.is_active:
			# the user is already active..
			return get_latest_entries(request, ACTIVATION_ERROR % ALREADY_ACTIVE)
		else:
			# get the profile of user
			profile = user.get_profile()
			delta = datetime.now() - profile.last_modified
			
			if delta.days > 3:
				# 3 days passed.. don't activate the user..
				return get_latest_entries(request, ACTIVATION_ERROR % ACTIVE_NONUSER)
				
			if profile.activation_key == key:
				user.is_active = True
				user.save()
			else:
				# keys doesn't match
				return get_latest_entries(request, ACTIVATION_ERROR % INVALID_ACTIVATION_CODE)
	else:
		# the user cannot be found..
		return get_latest_entries(request, ACTIVATION_ERROR % ACTIVE_NONUSER)

	return get_latest_entries(request, ACTIVATION_SUCCESS)

def register(request, template="users/registration.html"):
	# creating a captcha image
	captcha = create_captcha()

	if request.method == "POST":
		# creating a login form instance with post data
		form = RegistrationForm(request.POST)
		extra_context = {
			'form': form,
			'captcha': captcha,
		}
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			name = form.cleaned_data['name']
			surname = form.cleaned_data['surname']
			email = form.cleaned_data['email']
			if is_username_unique(username) and is_email_unique(email):
				# last, control the captcha and continue if it's correct
				test = lambda x={},y="": (x.has_key(y) and x[y] != "") or False
				if test(request.POST, "captcha_id") and test(request.POST, "registration_captcha"):
					cp = Captcha()
					cp.set_text(request.POST["registration_captcha"])
					if cp.generate_hash(settings.SECRET_KEY[:20]) == request.POST["captcha_id"]:
						# registering the user
						try:
							# the following line creates the user directly, it doesn't wait
							# for a save().. but firstname, lastname and activeness need
							# to be saved
							new_user = User.objects.create_user(username, email, password)
							new_user.first_name = name
							new_user.last_name = surname
							# new user will be passive 'til activation occurs
							new_user.is_active = False
							new_user.save()
							# creating a user profile with an activation key
							new_user.profile.create()
							# creating activation key
							profile = new_user.get_profile()
							profile.activation_key = create_activation_key()
							profile.save()
							# all done, now let's send him a mail for activation
							site = Site.objects.get(pk=1)
							send_mail(REGISTER_SUBJECT, 
									REGISTER_BODY % (site.name, site.domain, new_user.username, profile.activation_key, site.name), 
									settings.EMAIL_INFO_ADDRESS_TR, [email,], 
									fail_silently=settings.EMAIL_FAIL_SILENCE,
									auth_user=settings.EMAIL_HOST_USER, 
									auth_password=settings.EMAIL_HOST_PASSWORD)
							# leaving the "anonymous" user a new message..
							create_message(request, REG_SUCCESS)
							# redirecting the user to homepage
							return HttpResponseRedirect(reverse("blog"))
						except IntegrityError:
							# there's already a user with that name
							# normally this part shouldn't be invoked
							extra_context["error"] = u"Kayıtlı kullanıcı adı ya da e-posta adresi.. Lütfen başka bir kullanıcı adı ya da e-posta adresi seçin."
							return render_to_response(template, extra_context, context_instance=RequestContext(request))
					else:
						extra_context["error"] = u"Captcha hatalı ya da girilmemiş.."
						return render_to_response(template, extra_context, context_instance=RequestContext(request))
				else:
					extra_context["error"] = u"Captcha hatalı ya da girilmemiş.."
					return render_to_response(template, extra_context, context_instance=RequestContext(request))
			else:
				extra_context["error"] = u"Kayıtlı kullanıcı adı ya da e-posta adresi.. Lütfen başka bir kullanıcı adı ya da e-posta adresi seçin."
				return render_to_response(template, extra_context, context_instance=RequestContext(request))
		else:
			return render_to_response(template, extra_context, context_instance=RequestContext(request))
	else:
		# creating a login form instance
		form = RegistrationForm()
		extra_context = {
			'form': form,
			'captcha': captcha,
		}
		return render_to_response(template, extra_context, context_instance=RequestContext(request))

def user_logout(request):
	logout(request)
	if request.GET.has_key('next'):
		return HttpResponseRedirect(request.GET["next"])
	else:
		return HttpResponseRedirect(reverse("homepage"))

def user_login(request, template="users/login.html"):
	if request.method == "POST":
		# creating a login form instance with post data
		form = LoginForm(request.POST)
		extra_context = {
			'form': form,
		}
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			user = authenticate(username=username, password=password)
			if user is None:
				extra_context["error"] = u"Kullanıcı Adı ya da Şifre hatalı.. Lütfen tekrar deneyin.."
				return render_to_response(template, extra_context, context_instance=RequestContext(request))
			else:
				if user.is_active:
					login(request, user)
					# if there's a next parameter, then redirect the user
					# to where it has originally came from..
					if request.GET.has_key('next'):
						return HttpResponseRedirect(request.GET["next"])
					return HttpResponseRedirect(reverse("homepage"))
				else:
					# account disabled, redirecting to login page
					extra_context["error"] = u"Kullanıcı hesabınızı aktifleştirmeden kullanamazsınız."
					return render_to_response(template, extra_context, context_instance=RequestContext(request))
		else:
			extra_context["error"] = form.errors
			return render_to_response(template, extra_context, context_instance=RequestContext(request))
	else:
		# creating a login form instance
		form = LoginForm()
		extra_context = {
			'form': form,
		}
		return render_to_response(template, extra_context, context_instance=RequestContext(request))
