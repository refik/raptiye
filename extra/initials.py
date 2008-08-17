#!/usr/bin/env python
# encoding: utf-8

"""
initials.py

Does the necessary jobs after the initial
installation of raptiye..

Created by Alper KANAT on 2008-08-18.
Copyright (c) 2008 raptiye. All rights reserved.
"""

def create_anonymous_user():
	from django.conf import settings
	from django.contrib.auth.models import User
	user = User.objects.create_user("anonymous", settings.EMAIL_INFO_ADDRESS_EN, settings.ANONYMOUS_PASSWORD)
	user.first_name = "Anonymous"
	user.last_name = "User"
	user.save()
	user.profile.create()

def create_profile_for_first_user():
	"""
	When a Django application is first created,
	it asks permission to create a user who has
	the administrator privileges. Usually this 
	user doesn't have a profile..
	
	This method creates the profile for that user.
	"""
	from django.contrib.auth.models import User
	user = User.objects.get(pk=1)
	user.profile.create()

def main():
	create_anonymous_user()
	create_profile_for_first_user()

if __name__ == '__main__':
	main()