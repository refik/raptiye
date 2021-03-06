# coding: utf-8
# 
# raptiye
# Copyright (C) 2009  Alper KANAT <alperkanat@raptiye.org>
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
# along with this program. If not, see <http://www.gnu.org/licenses/>.
# 

from datetime import datetime
import re
	
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import simplejson

from raptiye.blog.views import get_latest_entries
from raptiye.comments.models import Comments
from raptiye.comments.views import create_captcha
from raptiye.extra.captcha import Captcha
from raptiye.extra.exceptions import *
from raptiye.extra.filters import is_username_unique, is_email_unique
from raptiye.extra.gravatar import get_gravatar
from raptiye.extra.mail import *
from raptiye.extra import messages
from raptiye.extra.openid_consumer import *
from raptiye.extra.session_data import create_data
from raptiye.users.forms import *

@login_required
def gravatar(request, username):
	if request.method == "POST" and request.POST.has_key("email"):
		site = Site.objects.get_current()
		email = request.POST["email"]
	return HttpResponse(get_gravatar(email, "http://" + site.domain + settings.DEFAULT_AVATAR))

@login_required
def notification_remove(request, username):
	# will return json object if the operation is successfull
	
	resp = {"status": 0}

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
			resp["status"] = 1
			return HttpResponse(simplejson.dumps(resp))
	else:
		resp["status"] = 1
		return HttpResponse(simplejson.dumps(resp))
	return HttpResponse(simplejson.dumps(resp))

@login_required
def profile(request, username, template="users/profile.html"):
	# FIXME: is the following line really necessary?
	# FIXME: the following code is too long.. shorten its logic..
	if request.user.is_authenticated() and request.user.username == username:
		# sometimes we need to log the user out
		logoutUser = False
		# getting the user information
		user = User.objects.get(username=username)
		profile = user.get_profile()
		
		extra_context = {
			"latest_comments": user.comments.order_by("-datetime")[:5],
			"watched_comments": user.comments.order_by("-datetime").filter(notification=True)[:5],
		}
		
		if request.method == 'POST':
			form = ProfileForm(request.POST)
			extra_context["form"] = form
			if form.is_valid():
				password = form.cleaned_data["password"]
				if password != "" and not user.check_password(password):
					user.set_password(password)
				user.first_name = form.cleaned_data["name"]
				user.last_name = form.cleaned_data["surname"]
				if form.cleaned_data["email"] != user.email:
					user.email = form.cleaned_data["email"]
					# turning on activation for user
					user.is_active = False
					profile.activation_key = create_activation_key()
					# mailing user for activation
					site = Site.objects.get_current()
					send_mail(settings.EMAIL_SUBJECT_PREFIX + messages.ACTIVATION_SUBJECT, 
							messages.ACTIVATION_BODY % (site.name, site.domain, user.username, profile.activation_key), 
							settings.EMAIL_INFO_ADDRESS_TR, [user.email,], 
							fail_silently=settings.EMAIL_FAIL_SILENCE,
							auth_user=settings.EMAIL_HOST_USER, 
							auth_password=settings.EMAIL_HOST_PASSWORD)
					logoutUser = True
				if form.cleaned_data["avatar"] != "":
					profile.avatar = form.cleaned_data["avatar"]
				profile.web_site = form.cleaned_data["website"]
				profile.openid = form.cleaned_data["openid"]
				# saving user and his profile
				user.save()
				profile.save()
				if logoutUser:
					logout(request)
				# leaving message to the user
				messages.set_user_message(request, messages.PROFILE_SUCCESS)
				# redirecting back to the profile page
				return HttpResponseRedirect(reverse("profile_page", args=[user.username]))
			else:
				return render_to_response(template, extra_context, context_instance=RequestContext(request))
		else:
			form = ProfileForm(initial={
					"username": user.username,
					"name": user.first_name,
					"surname": user.last_name,
					"email": user.email,
					"avatar": "" if user.get_profile().avatar == settings.DEFAULT_AVATAR else user.get_profile().avatar,
					"website": user.get_profile().web_site,
					"openid": user.get_profile().openid
				},
				auto_id=True)
			extra_context["form"] = form
		return render_to_response(template, extra_context, context_instance=RequestContext(request))
	else:
		# leaving a new message to the user..
		messages.set_user_message(request, messages.PROFILE_ACCOUNT_ERROR)
		# redirecting the user to blog
		return HttpResponseRedirect(reverse(settings.REDIRECT_URL))

def activation(request, username, key):
	if User.objects.filter(username=username).count() == 1:
		user = User.objects.get(username=username)
		if user.is_active:
			# the user is already active..
			messages.set_user_message(request, messages.ACTIVATION_ERROR % messages.ALREADY_ACTIVE)
		else:
			# get the profile of user
			profile = user.get_profile()
			delta = datetime.now() - profile.last_modified
			
			if delta.days > 3:
				# 3 days passed.. don't activate the user..
				messages.set_user_message(request, messages.ACTIVATION_ERROR % messages.ACTIVE_NONUSER)
				
			if profile.activation_key == key:
				user.is_active = True
				user.save()
				messages.set_user_message(request, messages.ACTIVATION_SUCCESS)
			else:
				# keys doesn't match
				messages.set_user_message(request, messages.ACTIVATION_ERROR % messages.INVALID_ACTIVATION_CODE)
	else:
		# the user cannot be found..
		messages.set_user_message(request, messages.ACTIVATION_ERROR % messages.ACTIVE_NONUSER)
	
	return HttpResponseRedirect(reverse(settings.REDIRECT_URL))

def register(request, template="users/registration.html"):
	# FIXME: the following code is too long.. shorten its logic..
	
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
					cp.text = request.POST["registration_captcha"]
					# validating captcha
					pattern = re.compile(u"[^a-zA-Z0-9]")
					if not pattern.search(cp.text) and cp.generate_hash(settings.SECRET_KEY[:20]) == request.POST["captcha_id"]:
						# registering the user
						try:
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
							site = Site.objects.get_current()
							send_mail(settings.EMAIL_SUBJECT_PREFIX + messages.REGISTER_SUBJECT, 
									messages.REGISTER_BODY % (site.name, site.domain, new_user.username, profile.activation_key, site.name), 
									settings.EMAIL_INFO_ADDRESS_TR, [email,], 
									fail_silently=settings.EMAIL_FAIL_SILENCE,
									auth_user=settings.EMAIL_HOST_USER, 
									auth_password=settings.EMAIL_HOST_PASSWORD)
							# leaving the "anonymous" user a new message..
							messages.set_user_message(request, messages.REG_SUCCESS)
							# redirecting the user to blog
							return HttpResponseRedirect(reverse(settings.REDIRECT_URL))
						except IntegrityError:
							# there's already a user with that name
							# normally this part shouldn't be invoked
							extra_context["error"] = messages.ALREADY_REGISTERED_USER
							return render_to_response(template, extra_context, context_instance=RequestContext(request))
					else:
						extra_context["error"] = messages.WRONG_CAPTCHA
						return render_to_response(template, extra_context, context_instance=RequestContext(request))
				else:
					extra_context["error"] = messages.WRONG_CAPTCHA
					return render_to_response(template, extra_context, context_instance=RequestContext(request))
			else:
				extra_context["error"] = messages.ALREADY_REGISTERED_USER
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

@login_required
def user_logout(request):
	logout(request)
	if request.GET.has_key('next'):
		return HttpResponseRedirect(request.GET["next"])
	else:
		return HttpResponseRedirect(reverse(settings.REDIRECT_URL))

def user_login(request, template="users/login.html"):
	# redirect the user to somewhere else if already login
	if request.user.is_authenticated():
		return HttpResponseRedirect(reverse(settings.REDIRECT_URL))
	
	# creating an OpenID form instance if allowed in settings
	openid_form = OpenIDForm() if settings.OPENID else None
	# creating a login form instance
	form = LoginForm()
	
	if request.method == "POST" and request.POST.has_key("form"):
		# choosing the form to process
		if request.POST["form"] == "openid":
			# creating an OpenID form instance with post data
			openid_form = OpenIDForm(request.POST)
			
			# checks for openid_form
			if openid_form.is_valid():
				identifier = openid_form.cleaned_data["identifier"]
				raptiye_openid = OpenID(request, reverse(settings.REDIRECT_URL), reverse("login_page"))
				try:
					publisher_url = raptiye_openid.authenticate(identifier, reverse("openid_complete"))
				except OpenIDProviderFailedError:
					messages.set_user_message(request, messages.OPENID_PROVIDER_FAILED)
					create_data(request, "form", "openid")
					return HttpResponseRedirect(reverse("login_page"))
				except OpenIDDiscoveryError:
					messages.set_user_message(request, messages.OPENID_DISCOVERY_FAILURE)
					create_data(request, "form", "openid")
					return HttpResponseRedirect(reverse("login_page"))
				return HttpResponseRedirect(publisher_url)
		elif request.POST["form"] == "login":
			# creating a login form instance with post data
			form = LoginForm(request.POST)
			
			# checks for login form
			if form.is_valid():
				username = form.cleaned_data['username']
				password = form.cleaned_data['password']
				user = authenticate(username=username, password=password)
				if user is None:
					messages.set_user_message(request, messages.LOGIN_ERROR)
					create_data(request, "form", "login")
					return HttpResponseRedirect(reverse("login_page"))
				else:
					if user.is_active:
						login(request, user)
						# if there's a next parameter, then redirect the user
						# to where it has originally came from..
						if request.GET.has_key('next'):
							return HttpResponseRedirect(request.GET["next"])
						return HttpResponseRedirect(reverse("blog"))
					else:
						# account disabled, redirecting to login page
						messages.set_user_message(request, messages.ACCOUNT_NEEDS_ACTIVATION)
						create_data(request, "form", "login")
						return HttpResponseRedirect(reverse("login_page"))
	
	# creating the dictionary with the forms (filled or not)
	extra_context = {
		'form': form,
		"openid_form": openid_form,
	}
	
	return render_to_response(template, extra_context, context_instance=RequestContext(request))

def forgotten_password(request, template="users/forgotten_password.html"):
	if request.method == "POST":
		form = ForgottenPasswordForm(request.POST)
		extra_context = {"form": form}

		if form.is_valid():
			email = form.cleaned_data["email"]
			# getting user who has that e-mail address
			if User.objects.filter(email=email).__len__() > 0:
				site = Site.objects.get_current()
				user = User.objects.get(email=email)
				# changing the user's password
				password = Captcha.generate_random_text()
				user.set_password(password)
				user.save()
				# mailing the new password to the user
				send_mail(settings.EMAIL_SUBJECT_PREFIX + messages.FORGOTTEN_PASSWORD_SUBJECT, 
						messages.FORGOTTEN_PASSWORD_BODY % (site.name, site.name, password), 
						settings.EMAIL_INFO_ADDRESS_TR, [user.email,], 
						fail_silently=settings.EMAIL_FAIL_SILENCE,
						auth_user=settings.EMAIL_HOST_USER, 
						auth_password=settings.EMAIL_HOST_PASSWORD)
				extra_context["status"] = True
			else:
				# can't find such a user
				extra_context["status"] = False
				extra_context["error"] = messages.FRG_CANNOT_FIND_EMAIL
	else:
		form = ForgottenPasswordForm()
		extra_context = {"form": form}

	return render_to_response(template, extra_context, context_instance=RequestContext(request))

def openid_complete(request):
	"""
	Completes the authentication process of OpenID..

	"""
	
	if settings.OPENID:
		raptiye_openid = OpenID(request, reverse(settings.REDIRECT_URL), reverse("login_page"))
		# getting query string params
		params = dict(request.GET.items())
		openid_response = raptiye_openid.complete(params, reverse("openid_complete"))
		# checking for the necessary info in the response
		if openid_response.has_key("identifier") and openid_response.has_key("user_info"):
			# authenticate the user or create a raptiye user with profile
			try:
				user = authenticate(identifier=openid_response["identifier"], user_info=openid_response["user_info"])
				if user is None:
					messages.set_user_message(request, messages.OPENID_AUTH_FAILURE)
				else:
					login(request, user)
					# if there's a next parameter, then redirect the user
					# to where it has originally came from..
					if request.GET.has_key('next'):
						return HttpResponseRedirect(request.GET["next"])
					return HttpResponseRedirect(reverse(settings.REDIRECT_URL))
			except OpenIDUsernameExistsError:
				messages.set_user_message(request, messages.OPENID_EXISTING_USERNAME)

	return HttpResponseRedirect(reverse("login_page"))

