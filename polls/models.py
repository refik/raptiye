from django.db import models

class Poll(models.Model):
	"Stores the general poll information"
	question = models.CharField(u"Question", max_length=200)
	datetime = models.DateTimeField(u"Created On", auto_now_add=True)
	published = models.BooleanField(u"Is Published", default=False)
	
	def __unicode__(self):
		return self.question
	
	def get_results(self):
		results = u""
		for choice in self.choices.all():
			results += u"<strong>&raquo;</strong> %s <strong>(%d)</strong><br>" % (choice.choice, choice.votes)
		return results
	
	get_results.short_description = u"Results for Poll"
	get_results.allow_tags = True
	
	class Meta:
		get_latest_by = "datetime"
		ordering = ["-datetime", "question"]
		verbose_name = u"Poll"
		verbose_name_plural = u"Polls"

class Choice(models.Model):
	"Stores the essential information about the poll.."
	poll = models.ForeignKey(Poll, related_name="choices", verbose_name=u"Poll")
	choice = models.CharField(u"Choice", max_length=200)
	votes = models.IntegerField(u"Votes", blank=True, default=0, editable=False)
	
	def __unicode__(self):
		return self.choice
	
	class Meta:
		ordering = ["choice"]
		verbose_name = u"Choice"
		verbose_name_plural = u"Choices"