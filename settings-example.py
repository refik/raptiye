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

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Alper KANAT', 'alperkanat@raptiye.org'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = '%s/raptiye.db' % DOCUMENT_ROOT
DATABASE_USER = ''
DATABASE_PASSWORD = ''
DATABASE_HOST = ''
DATABASE_PORT = ''

TIME_ZONE = 'Europe/Istanbul'

LANGUAGE_CODE = 'tr'
DEFAULT_CHARSET='utf8'
DEFAULT_CONTENT_TYPE = 'text/html'
FILE_CHARSET = 'utf-8'

SITE_ID = 1

USE_I18N = True

MEDIA_ROOT = '%s/media/' % DOCUMENT_ROOT

MEDIA_URL = '/media/'

ADMIN_MEDIA_PREFIX = '/media/admin/'

# fill this with a newly created django app's secret key
SECRET_KEY = ''

TEMPLATE_LOADERS = (
	'django.template.loaders.filesystem.load_template_source',
	'django.template.loaders.app_directories.load_template_source',
)

MIDDLEWARE_CLASSES = (
	'django.middleware.common.CommonMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.middleware.doc.XViewMiddleware',
	'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
	'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware'
)

ROOT_URLCONF = 'raptiye.urls'

TEMPLATE_DIRS = (
	"%s/templates/" % DOCUMENT_ROOT,
)

INSTALLED_APPS = (
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.redirects',
	'django.contrib.sessions',
	'django.contrib.sites',
	'django.contrib.flatpages',
	'raptiye.blog',
	'raptiye.comments',
	'raptiye.frontpage',
	'raptiye.tags',
	'raptiye.users',
	'raptiye.links',
	'raptiye.polls',
	# the following app(s) aren't mandatory and will be removed
	# when django has the functionality
	'raptiye.contrib.session_messages',
)

TEMPLATE_CONTEXT_PROCESSORS = (
	"django.core.context_processors.auth",
	"django.core.context_processors.debug",
	"django.core.context_processors.i18n",
	"django.core.context_processors.media",
	"django.core.context_processors.request",
	"raptiye.contrib.session_messages.context_processors.session_messages",
)

AUTHENTICATION_BACKENDS = (
	'django.contrib.auth.backends.ModelBackend',
	'raptiye.users.backends.OpenIDBackend',
)

ADMIN_LIST_PER_PAGE = 20
ENTRIES_PER_PAGE = 5
LANGUAGES = (
	("tr", "tr"),
	("en", "en"),
)

AUTH_PROFILE_MODULE = 'users.UserProfile'
# this is to serve temporary images like captcha..
TEMP_MEDIA_PREFIX = 'temp/'
# how many times a user can regenerate captchas consequtively
CAPTCHA_RENEWAL_LIMIT = 10
# how many minutes of penaly will be applied..
CAPTCHA_PENALTY = 10

# this address is used for notifications
EMAIL_INFO_ADDRESS_TR = "bilgi@raptiye.org"

# MAIL SETTINGS (needs to be changed..)
EMAIL_HOST = ""
# EMAIL_PORT = 
EMAIL_HOST_USER = EMAIL_INFO_ADDRESS_TR
EMAIL_HOST_PASSWORD = ""
EMAIL_SUBJECT_PREFIX = u"[raptiye] "
EMAIL_USE_TLS = False
EMAIL_FAIL_SILENCE = False

# default avatar for all users..
DEFAULT_AVATAR = "/media/images/default_avatar.png"

# LOCALE settings may differ on different platforms
LOCALES = {
	'tr': 'tr_TR.utf-8',
	'en': 'en_US.utf-8',
}

VERSION = '1.0.3'

ANONYMOUS_PASSWORD = ""
LATEST_COMMENTS_LIMIT = 5

# enable or disable writing comments anonymously
ALLOW_ANONYMOUS_COMMENTS = True

# twitter credentials
TWITTER_USERNAME = ""
TWITTER_PASSWORD = ""
TWITTER_LIMIT = 5
POST_TO_TWITTER = True

# colorize the code in entries
COLORIZE_CODE = True

# OpenID Support
OPENID = True
OPENID_PASSWORD_FOR_NEW_USER = ""

LOGIN_URL = "/users/login/"
LOGOUT_URL = "/users/logout/"

# URL Pattern Naming used here..
REDIRECT_URL = "blog"