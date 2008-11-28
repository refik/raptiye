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

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Alper KANAT', 'alperkanat@raptiye.org'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'sqlite3'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = 'raptiye'             # Or path to database file if using sqlite3.
DATABASE_USER = ''             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Istanbul'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'tr'
DEFAULT_CHARSET='utf8'
DEFAULT_CONTENT_TYPE = 'text/html'
FILE_CHARSET = 'utf-8'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = '/Users/alperkanat/Projects/raptiye/media/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = 'http://localhost:8000/media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/admin/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '=qz$*=u$3(9d%mhi(y)(ur&v)vg&!tw#m0_&xjr%p_$ksh61jq'

# List of callables that know how to import templates from various sources.
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
	"/Users/alperkanat/Projects/raptiye/templates/",
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

VERSION = '1.0.2'

ANONYMOUS_PASSWORD = ""
LATEST_COMMENTS_LIMIT = 5

# enable or disable writing comments anonymously
ALLOW_ANONYMOUS_COMMENTS = True

# twitter credentials
TWITTER_USERNAME = ""
TWITTER_PASSWORD = ""
TWITTER_LIMIT = 5

# colorize the code in entries
COLORIZE_CODE = True