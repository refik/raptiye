#-*- coding: utf-8 -*-
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

import os, sys

try:
	import django
except ImportError:
	sys.stderr.write("django couldn't be found.")
	sys.exit(1)

DOCUMENT_ROOT = os.path.abspath(os.path.dirname(__file__))
DJANGO_DIR = os.path.abspath(os.path.dirname(django.__file__))



# --- GENERIC SETTINGS --------------

PROJECT_NAME = u"raptiye"
VERSION = '2.0'

CSRF_COOKIE_DOMAIN = ".raptiye.org"

DEFAULT_CHARSET='utf8'
DEFAULT_CONTENT_TYPE = 'text/html'
FILE_CHARSET = 'utf-8'

LANGUAGES = (
	("tr", "tr"),
	("en", "en"),
)

AUTHENTICATION_BACKENDS = (
	'django.contrib.auth.backends.ModelBackend',
	'raptiye.users.backends.OpenIDBackend',
)



# --- ADMIN SETTINGS --------------

ADMIN_LIST_PER_PAGE = 20
AUTH_PROFILE_MODULE = 'users.UserProfile'



# --- COMMENT SETTINGS --------------

# default avatar for all users..
DEFAULT_AVATAR = "/media/images/default_avatar.png"

# this is to serve temporary images like captcha..
TEMP_MEDIA_PREFIX = 'temp/'

# how many minutes of penaly will be applied..
CAPTCHA_PENALTY = 10
# how many times a user can regenerate captchas consequtively
CAPTCHA_RENEWAL_LIMIT = 10

ALLOW_ANONYMOUS_COMMENTS = True
LATEST_COMMENTS_LIMIT = 5



# --- TWITTER SETTINGS --------------

POST_TO_TWITTER = False
ENABLE_TWITTER_BOX = False
TWITTER_USERNAME = ""
TWITTER_PASSWORD = ""
TWITTER_LIMIT = 5



# --- OTHER SETTINGS --------------

OPENID = False

COLORIZE_CODE = False
ENABLE_EMOTIONS = True
ENTRIES_PER_PAGE = 8

EMAIL_FAIL_SILENCE = True
EMAIL_HOST = ""
EMAIL_HOST_PASSWORD = ""
EMAIL_HOST_USER = "bilgi@raptiye.org"
EMAIL_INFO_ADDRESS_TR = "bilgi@raptiye.org"
EMAIL_INFO_ADDRESS_EN = "bilgi@raptiye.org"
# EMAIL_PORT = 
EMAIL_SUBJECT_PREFIX = u"[raptiye] "
EMAIL_USE_TLS = True

LOCALES = {
	'tr': 'tr_TR.utf-8',
	'en': 'en_US.utf-8',
}

LOGIN_URL = "/users/login/"
LOGOUT_URL = "/users/logout/"

# URL Pattern Naming used here..
REDIRECT_URL = "blog"



# --- STANDARD DJANGO SETTINGS --------------

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Alper KANAT', 'alperkanat@raptiye.org'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'sqlite3'
DATABASE_HOST = ''
DATABASE_NAME = '%s/raptiye.db' % DOCUMENT_ROOT
DATABASE_PASSWORD = ''
DATABASE_PORT = ''
DATABASE_USER = ''

TIME_ZONE = 'Europe/Istanbul'

LANGUAGE_CODE = 'tr'

SITE_ID = 1

USE_I18N = True

MEDIA_ROOT = '%s/media/' % DOCUMENT_ROOT

MEDIA_URL = '/media/'

ADMIN_MEDIA_PREFIX = '/media/admin/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = ''

MIDDLEWARE_CLASSES = (
	'django.middleware.common.CommonMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.middleware.doc.XViewMiddleware',
	'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
	'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware'
)

ROOT_URLCONF = 'raptiye.urls'

TEMPLATE_CONTEXT_PROCESSORS = (
	"django.core.context_processors.auth",
	"django.core.context_processors.debug",
	"django.core.context_processors.i18n",
	"django.core.context_processors.media",
	"django.core.context_processors.request",
	"raptiye.extra.session_data.session_data",
)

TEMPLATE_DIRS = (
	"%s/templates/" % DOCUMENT_ROOT,
)

TEMPLATE_LOADERS = (
	'django.template.loaders.filesystem.load_template_source',
	'django.template.loaders.app_directories.load_template_source',
)

INSTALLED_APPS = (
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.flatpages',
	'django.contrib.redirects',
	'django.contrib.sessions',
	'django.contrib.sites',
	'raptiye.blog',
	'raptiye.comments',
	'raptiye.frontpage',
	'raptiye.links',
	'raptiye.polls',
	'raptiye.tags',
	'raptiye.users',
)

try:
    from raptiye.local_settings import *
except ImportError:
    pass

