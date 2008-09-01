#-*- encoding: utf-8 -*-

from django.http import HttpResponse
from django.utils import simplejson
from raptiye.extra.messages import POLL_ERROR
from raptiye.polls.models import Poll

def polls(request):
	# the response is returned as json object with
	# all parameters embedded into..
	response = {
		"status": 0,
	}
	
	# used to test if a variable is inside the dict. or not
	test = lambda x={},y="": (x.has_key(y) and x[y] != "") or False
	
	# stores the data that will be used in the template
	answers = []
	
	if request.method == "POST":
		# if the poll is not submitted show the form to let user submit
		# otherwise show the poll results
		if not test(request.session, "poll_submitted"):
			if test(request.POST, "poll") and test(request.POST, "poll_answer"):
				poll = Poll.objects.get(id=request.POST["poll"])
				choice = poll.choices.get(id=request.POST["poll_answer"])
				# incrementing choice's vote
				choice.votes += 1
				# saving the choice
				choice.save()
				# setting a key to the session for the user
				request.session["poll_submitted"] = True
				# returning the results
				for answer in poll.choices.all():
					answers.append({"name": answer.choice, "votes": answer.votes})
				# storing all data to the response
				response["result"] = answers
				# returning the json encoded version of response data..
				return HttpResponse(simplejson.dumps(response))
		else:
			if test(request.POST, "poll"):
				poll = Poll.objects.get(id=request.POST["poll"])
				# returning the results
				for answer in poll.choices.all():
					answers.append({"name": answer.choice, "votes": answer.votes})
				# storing all data to the response
				response["result"] = answers
				# returning the json encoded version of response data..
				return HttpResponse(simplejson.dumps(response))
	
	# this part works if the if part somehow sucks
	response["status"] = 1
	response["error"] = POLL_ERROR
	return HttpResponse(simplejson.dumps(response))