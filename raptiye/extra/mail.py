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

from django.conf import settings

from raptiye.extra import messages

def send_comment_notification(entry, user):
	from django.core.mail import send_mass_mail
	
	notifications = [(messages.COMMENT_NOTIFICATION_SUBJECT, messages.COMMENT_NOTIFICATION_MESSAGE % (entry.title, entry.get_full_url()),
		settings.EMAIL_INFO_ADDRESS_TR, [comment.author.email])
		for comment in entry.comments.filter(published=True, notification=True).exclude(author=user)]
	
	send_mass_mail(notifications, settings.EMAIL_FAIL_SILENCE)

def create_activation_key():
	from random import sample
	import sha, string
	choices = list(string.letters + string.digits)
	return sha.new(settings.SECRET_KEY[:20] + "".join(sample(choices, 5))).hexdigest()

