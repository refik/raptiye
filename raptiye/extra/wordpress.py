#!/usr/bin/env python
# encoding: utf-8
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

"""
wordpress.py

This module aims to import all necessary data from Wordpress blogs..

Since comments in Wordpress can be written by Anonymous users (which 
raptiye doesn't let), the importer assigns all previous comments to the
Anonymous user of raptiye.. No other "new" comment can be owned by 
Anonymous user..

I don't care about the registered users in Wordpress.. Therefore I'm not
importing them.. There were several users which were probably created by 
some spam makers.. raptiye has captcha and moderation "for once" for 
that..

The importer works just for MySQL.. Therefore you need to have necessary 
packages like python-mysql..

The script assumes that you've already installed the necessary tables for
your Django applications initially and there's no data written in it!
"""

# Development MySQL Server Settings
DEV_SERVER_HOST = "localhost"
DEV_SERVER_PORT = 3306
DEV_SERVER_USERNAME = "raptiye"
DEV_SERVER_PASSWD = "test"
DEV_SERVER_DBNAME = "wordpress"
DEV_SERVER_CHARSET = "utf8"

# Fields for each WordPress table
comments = {"table": "wp_comments", "fields": ("comment_author", "comment_author_email", "comment_author_url", "comment_date", "comment_content", "comment_approved")}
links = {"table": "wp_links", "fields": ("link_url", "link_name", "link_target", "link_category", "link_description")}
# WordPress link categories sucks! Have to hardcode it.. :(
links_dict = {
	"0": u"Girilesiceler",
	"2": u"Arkadaşlar",
	"3": u"Girilesiceler",
}
posts = {"table": "wp_posts", "fields": ("ID", "post_date", "post_content", "post_title", "comment_status")}
# WordPress tags database structure really sucks! Tags are stored in many tables with relationships
# between them.. Therefore I'm hardcoding it's SQL syntax in the importer.. Damn, this importer 
# sucks too! :S
tags = {"table": "wp_terms", "fields": ("name",)}

# import starts after this point..

import sys
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from raptiye.blog.models import Entry
from raptiye.comments.models import Comments
from raptiye.links.models import *
from raptiye.tags.models import Tag

try:
	import MySQLdb
except ImportError:
	print "MySQL bindings for Python is missing.. Please try again later.."
	sys.exit(1)

# trying to connect to the development MySQL server
print "Connecting to the MySQL database...",
try:
	devs = MySQLdb.connect(host=DEV_SERVER_HOST, port=DEV_SERVER_PORT, user=DEV_SERVER_USERNAME, passwd=DEV_SERVER_PASSWD, db=DEV_SERVER_DBNAME, charset=DEV_SERVER_CHARSET)
except MySQLdb.OperationalError:
	print "Cannot connect to development MySQL server.."
	sys.exit(1)
print "done!"

try:
	anonymous = User.objects.get(username="anonymous")
except User.DoesNotExist:
	print "Anonymous user doesn't exist. Make sure you've ran Initials() before.."
	sys.exit(1)

# creating cursor for development server
dc = devs.cursor()

# Getting tags..
print "Getting tags...",
query = "select %s from %s" % (", ".join(tags["fields"]), tags["table"])
dc.execute(query)
result = dc.fetchall()
print "done!"
print "Creating tag objects...",
# Creating tag objects
for row in result:
	Tag.objects.create(name=row[0])
print "done!"

# Getting blog entries with tags related..
print "Getting blog entries with tags related...",
query = "select %s from %s where post_status='publish'" % (", ".join(posts["fields"]), posts["table"])
dc.execute(query)
result = dc.fetchall()
print "done!"
# Creating entry objects
print "Creating blog entries (with tags and comments) and this process may take long...",
for row in result:
	e = Entry()
	e.id = row[0]
	e.datetime = row[1]
	e.content = row[2]
	e.title = row[3]
	e.published = True
	e.comments_enabled = True if row[4] == "open" else False
	e.slug = slugify(e.title)
	# getting all tags for entry
	tags_subquery = """select terms.name 
		from wp_terms terms, wp_term_relationships relations, wp_term_taxonomy taxonomy 
		where relations.object_id=%d and relations.term_taxonomy_id=taxonomy.term_taxonomy_id 
			and terms.term_id=taxonomy.term_id""" % e.id
	dc.execute(tags_subquery)
	tags_of_entry = dc.fetchall()
	# associating tags with entry
	for tag in tags_of_entry:
		e.tags.add(Tag.objects.get(name=tag[0]))
	e.save()
	# getting all comments for entry
	comments_subquery = "select %s from %s where comment_post_ID=%d and comment_approved != 'spam'" % (", ".join(comments["fields"]), comments["table"], e.id)
	dc.execute(comments_subquery)
	comments_of_entry = dc.fetchall()
	# creating and associating comments with entry
	# all comments belong to anonymous user.. so please make
	# sure that you've ran Initials() before!
	if comments_of_entry.__len__() > 0:
		for comment in comments_of_entry:
			c = Comments()
			c.entry = e
			c.author = anonymous
			c.anonymous_author = comment[0]
			c.anonymous_author_email = comment[1]
			c.anonymous_author_web_site = comment[2]
			c.datetime = comment[3]
			c.content = comment[4]
			c.published = True if comment[5] == "1" else False
			c.save()
print "done!"

# Creating link categories (hardcode)
print "Creating link categories (hardcode)...",
LinkCategories.objects.create(title=u"Arkadaşlar", image=u"/media/images/friends.png", level=1)
LinkCategories.objects.create(title=u"Girilesiceler", image=u"/media/images/links.png", level=2)

# Getting links
print "Getting links...",
query = "select %s from %s" % (", ".join(links["fields"]), links["table"])
dc.execute(query)
result = dc.fetchall()
print "done!"
print "Creating link objects...",
for row in result:
	link = Links()
	link.url = row[0]
	link.title = row[1]
	link.window = True if row[2] == '_blank' else False
	link.category = LinkCategories.objects.get(title=links_dict[row[3].__str__()])
	link.description = row[4]
	link.save()
print "done!"

print "Everything is successfull.. :) You're on your lucky day.. Exiting.."
sys.exit(0)