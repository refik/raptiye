from django.contrib.auth.models import User

def is_username_unique(value):
	if User.objects.filter(username=value).count() == 0:
		return True
	else:
		return False

def is_email_unique(value):
	if User.objects.filter(email=value).count() == 0:
		return True
	else:
		return False
