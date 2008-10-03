#-*- encoding: utf-8 -*-
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

from django.http import HttpResponse
from django.utils import simplejson
from raptiye.extra.messages import POLL_ERROR
from raptiye.polls.models import Poll

# used to test if a variable is inside the dict. or not
test = lambda x={},y="": (x.has_key(y) and x[y] != "") or False

def polls(request):
	# the resp is returned as json object with
	# all parameters embedded into..
	resp = {
		"status": 0,
	}
	
	# stores the data that will be used in the template
	answers = []
	
	if request.method == "POST":
		# if the poll is not submitted show the form to let user submit
		# otherwise show the poll results
		if not test(request.COOKIES, "poll_submitted"):
			if test(request.POST, "poll") and test(request.POST, "poll_answer"):
				poll = Poll.objects.get(id=request.POST["poll"])
				choice = poll.choices.get(id=request.POST["poll_answer"])
				# incrementing choice's vote
				choice.votes += 1
				# saving the choice
				choice.save()
				# setting a key to the cookie for the user
				response = HttpResponse()
				response.set_cookie("poll_submitted", True)
				# returning the results
				for answer in poll.choices.all():
					answers.append({"name": answer.choice, "votes": answer.votes})
				# storing all data to the resp
				resp["result"] = answers
				# returning the json encoded version of resp data..
				response.content = simplejson.dumps(resp)
				return response
			else:
				# this part could be controlled by an elif statement
				# but it's already checked in getResultsForPoll function..
				results = getResultsForPoll(request)
				return HttpResponse(results)
		else:
			results = getResultsForPoll(request)
			return HttpResponse(results)
	
	# this part works if the if part somehow sucks
	resp["status"] = 1
	resp["error"] = POLL_ERROR
	return HttpResponse(simplejson.dumps(resp))

def getResultsForPoll(request):
	# the resp is returned as json object with
	# all parameters embedded into..
	resp = {
		"status": 0,
	}
	
	# stores the data that will be used in the template
	answers = []
	
	if test(request.POST, "poll"):
		poll = Poll.objects.get(id=request.POST["poll"])
		# returning the results
		for answer in poll.choices.all():
			answers.append({"name": answer.choice, "votes": answer.votes})
		# storing all data to the resp
		resp["result"] = answers
		# returning the json encoded version of resp data..
		return simplejson.dumps(resp)