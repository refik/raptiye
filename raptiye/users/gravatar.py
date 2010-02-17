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

import urllib, hashlib

def get_gravatar(email, default, size=50):
	gravatar_url = "http://www.gravatar.com/avatar.php?"
	gravatar_url += urllib.urlencode({"gravatar_id": hashlib.md5(email).hexdigest(), 
		"default": default, "size": str(size)})
	return gravatar_url
