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

"""
A very basic module that makes a request to the hidden
TinyURL API with a given URL and returns the TinyURL..

"""

import urllib

def shorten_url(url):
    api_url = "http://tinyurl.com/api-create.php"

    if len(url) > 30:
        try:
            resp = urllib.urlopen(api_url, "url=" + url)
            return resp.read()
        except IOError:
            return url
    else:
        return url
