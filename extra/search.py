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

from django.db.models import Q
from raptiye.blog.models import Entry

class SearchAgainstEntries():
	"""
	searches against the fields title, content and tags
	of each blog entry and returns the OR'ed list..

	the result is ordered by datetime which means the 
	latest post will be the first one in the list..
	"""

	def __init__(self, keywords=""):
		self.keyword_list = keywords.split(" ")
	
	def get_keyword_list(self):
		return self.keyword_list

	def result(self):
		# nice or_ interface instead of a | b - amazing.. :)
		import operator

		q_list = []

		# creating a list of Q objects
		for keyword in self.get_keyword_list():
			q_list.append(Q(title__icontains=keyword) | Q(content__icontains=keyword) | Q(tags__name__iexact=keyword))

		# creating an OR'ed Q from the list
		final_q = reduce(operator.or_, q_list)

		return Entry.objects.filter(final_q).exclude(sticky=True).order_by("-datetime").distinct()
