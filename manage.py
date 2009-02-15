#!/usr/bin/env python
#-*- encoding: utf-8 -*-
# 
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

import os
import re
import shutil
import sys
from django.core.exceptions import ImproperlyConfigured
from random import choice
from raptiye import settings_example
from raptiye.extra import messages

def get_dependency_msg(error):
	"""
	Hack for transforming messages when database
	backends are not found. Currently I've opened
	#10270 for this purpose..
	
	"""
	if error.find("psycopg") > 0:
		return messages.POSTGRESQL_NOT_FOUND
	elif error.find("psycopg2") > 0:
		return messages.POSTGRESQL2_NOT_FOUND
	elif error.find("MySQLdb") > 0:
		return messages.MYSQL_NOT_FOUND
	elif error.find("cx_Oracle") > 0:
		return messages.ORACLE_NOT_FOUND
	else:
		return messages.INVALID_DB_BACKEND

try:
	from django.core.management import execute_manager
except ImportError:
	sys.stderr.write(messages.DJANGO_NOT_FOUND)
	sys.exit(1)

try:
	import settings # Assumed to be in the same directory.
except ImportError:
	sys.stderr.write(messages.SETTINGS_NOT_FOUND)
	
	# copy sample settings file into a real one
	shutil.copy2("settings_example.py", "settings.py")
	
	# reading the settings file..
	file_path = os.path.join(settings_example.DOCUMENT_ROOT, "settings.py")
	settings_content = open(file_path).read()
	
	# creating a new secret key
	secret_key = ''.join([choice('abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)') for i in range(50)])
	settings_content = re.sub(r"(?<=SECRET_KEY = ')'", secret_key + "'", settings_content)
	
	# TODO: dependency checks
	
	# updating settings file
	with open(file_path, "w") as settings_file:
		settings_file.write(settings_content)
	
	# import newly created settings
	import settings

if __name__ == "__main__":
	if len(sys.argv) > 1:
		try:
			execute_manager(settings)
		except ImproperlyConfigured, e:
			sys.stderr.write(get_dependency_msg(unicode(e)))
			sys.exit(1)
	else:
		# running syncdb
		execute_manager(settings, [__file__, "syncdb"])
		# running initial stuff for raptiye
		from raptiye.extra import initials
		initials.create_anonymous_user()
		initials.create_profile_for_first_user()
		# running the development server
		execute_manager(settings, [__file__, "runserver"])