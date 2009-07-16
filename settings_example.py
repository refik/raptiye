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

DOCUMENT_ROOT = os.path.abspath(os.path.dirname(__file__))


# --- ADMIN SETTINGS ------------------------

ADMIN_LIST_PER_PAGE = 20
AUTH_PROFILE_MODULE = 'users.UserProfile'

EMAIL_FAIL_SILENCE = True
EMAIL_HOST = ""
EMAIL_HOST_PASSWORD = ""
EMAIL_HOST_USER = "bilgi@raptiye.org"
# this address is used for notifications
EMAIL_INFO_ADDRESS_TR = "bilgi@raptiye.org"
# EMAIL_PORT = 
EMAIL_SUBJECT_PREFIX = u"[raptiye] "
EMAIL_USE_TLS = False

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

LANGUAGES = (
	("tr", "tr"),
	("en", "en"),
)

LOGIN_URL = "/users/login/"
LOGOUT_URL = "/users/logout/"

# URL Pattern Naming used here..
REDIRECT_URL = "blog"

SECRET_KEY = ''

# this is to serve temporary images like captcha..
TEMP_MEDIA_PREFIX = 'temp/'


# --- BLOG SETTINGS -------------------------

# colorize the code in entries
COLORIZE_CODE = False
ENABLE_EMOTIONS = True
ENTRIES_PER_PAGE = 8


# --- CAPTCHA SETTINGS ----------------------

# how many minutes of penaly will be applied..
CAPTCHA_PENALTY = 10
# how many times a user can regenerate captchas consequtively
CAPTCHA_RENEWAL_LIMIT = 10


# --- COMMENT SETTINGS ----------------------

# enable or disable writing comments anonymously
ALLOW_ANONYMOUS_COMMENTS = True
LATEST_COMMENTS_LIMIT = 5


# --- DATABASE SETTINGS ---------------------

DATABASE_ENGINE = 'sqlite3'
DATABASE_HOST = ''
DATABASE_NAME = '%s/raptiye.db' % DOCUMENT_ROOT
DATABASE_PASSWORD = ''
DATABASE_PORT = ''
DATABASE_USER = ''


# --- DEBUG SETTINGS ------------------------

ADMINS = (
    ('Alper KANAT', 'alperkanat@raptiye.org'),
)

AUTHENTICATION_BACKENDS = (
	'django.contrib.auth.backends.ModelBackend',
	'raptiye.users.backends.OpenIDBackend',
)

DEBUG = False
TEMPLATE_DEBUG = DEBUG
MANAGERS = ADMINS


# --- DJANGO INTERNAL SETTINGS --------------

MIDDLEWARE_CLASSES = (
	'django.middleware.common.CommonMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.middleware.doc.XViewMiddleware',
	'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
	'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware'
)

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


# --- LANGUAGE SETTINGS ---------------------

DEFAULT_CHARSET='utf8'
DEFAULT_CONTENT_TYPE = 'text/html'
FILE_CHARSET = 'utf-8'
LANGUAGE_CODE = 'tr'

LOCALES = {
	'tr': 'tr_TR.utf-8',
	'en': 'en_US.utf-8',
}

USE_I18N = True


# --- PROFILE SETTINGS ----------------------

# default avatar for all users..
DEFAULT_AVATAR = "/media/images/default_avatar.png"


# --- RAPTIYE SETTINGS ----------------------

PROJECT_NAME = u"raptiye"
VERSION = '1.0.6'


# --- TIME SETTINGS -------------------------

TIME_ZONE = 'Europe/Istanbul'


# --- TWITTER SETTINGS ----------------------

POST_TO_TWITTER = False
ENABLE_TWITTER_BOX = False
TWITTER_USERNAME = ""
TWITTER_PASSWORD = ""
TWITTER_LIMIT = 5


# --- OPENID SETTINGS -----------------------

OPENID = True


# --- URL SETTINGS --------------------------

ADMIN_MEDIA_PREFIX = '/media/admin/'
MEDIA_ROOT = '%s/media/' % DOCUMENT_ROOT
MEDIA_URL = '/media/'
ROOT_URLCONF = 'raptiye.urls'
SITE_ID = 1