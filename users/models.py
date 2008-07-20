from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
	user = models.ForeignKey(User, verbose_name=u"User")
	avatar = models.URLField(u"Avatar", default=settings.DEFAULT_AVATAR)
	web_site = models.URLField(u"Web Site", blank=True)
	activation_key = models.CharField(u"Aktivasyon Kodu", max_length=100, blank=True)

	def __unicode__(self):
		return "User Profile of %s" % self.user.username

	class Meta:
		verbose_name = u"User Profile"
		verbose_name_plural = u"User Profiles"
