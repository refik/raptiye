#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import os, sys
from raptiye.extra import messages

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

if __name__ == "__main__":
	execute_manager(settings)