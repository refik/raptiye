#-*- encoding: utf-8 -*-

import urllib, hashlib

def get_gravatar(email, default, size=50):
	gravatar_url = "http://www.gravatar.com/avatar.php?"
	gravatar_url += urllib.urlencode({"gravatar_id": hashlib.md5(email).hexdigest(), 
		"default": default, "size": str(size)})
	return gravatar_url
