#!/usr/bin/env python
# encoding: utf-8

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
DEV_SERVER_DBNAME = "raptiye"
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
from django.template.defaultfilters import slugify
from raptiye.tags.models import Tag
from raptiye.blog.models import Entry

try:
	import MySQLdb
except ImportError:
	print "MySQL bindings for Python is missing.. Please try again later.."
	sys.exit(1)

# trying to connect to the development MySQL server
try:
	devs = MySQLdb.connect(host=DEV_SERVER_HOST, port=DEV_SERVER_PORT, user=DEV_SERVER_USERNAME, passwd=DEV_SERVER_PASSWD, db=DEV_SERVER_DBNAME, charset=DEV_SERVER_CHARSET)
except MySQLdb.OperationalError:
	print "Cannot connect to development MySQL server.."
	sys.exit(1)

# creating cursor for development server
dc = devs.cursor()

# Getting tags..
query = "select %s from %s" % (", ".join(tags["fields"]), tags["table"])
dc.execute(query)
result = dc.fetchall()
# Creating tag objects
for row in result:
	row[0]

# # Getting blog entries with tags related..
# query = "select %s from %s where post_status='publish'" % (", ".join(posts["fields"]), posts["table"])
# dc.execute(query)
# result = dc.fetchall()
# # Creating entry objects
# for row in result:
# 	e = Entry()
# 	e.id = row[0]
# 	e.datetime = row[1]
# 	e.content = row[2]
# 	e.title = row[3]
# 	e.published = True
# 	e.comments_enabled = row[4] == "open" ? True : False
# 	e.slug = slugify(e.title)
# 	# getting all tags for entry
# 	subquery = """select terms.name 
# 		from wp_terms terms, wp_term_relationships relations, wp_term_taxonomy taxonomy 
# 		where relations.object_id=%d and relations.term_taxonomy_id=taxonomy.term_taxonomy_id 
# 			and terms.term_id=taxonomy.term_id""" % e.id