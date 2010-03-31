#!/usr/bin/env python
# coding: utf-8

"""
Imports legacy tag data to raptiye 2.0 which uses
django-tagging

"""

import sqlite3

from raptiye.blog.models import Entry

conn = sqlite3.connect("raptiye.db")
cur = conn.cursor()
tag_list = cur.execute("select * from tags_tag").fetchall()
tags = {}

for tag in tag_list:
    if tag[1] == u"Debian GNU/Linux":
        tags[tag[0]] = u"debian"
    elif tag[1] == u"Işık Üniversitesi":
        tags[tag[0]] = u"ışık üniversitesi"
    else:
        tags[tag[0]] = tag[1]

tag_relation_list = cur.execute("select entry_id, tag_id from blog_entry_tags").fetchall()
tag_relations = {}

for relation in tag_relation_list:
    if tag_relations.has_key(relation[0]):
        tag_relations[relation[0]].append(relation[1])
    else:
        tag_relations[relation[0]] = [relation[1],]

for relation in tag_relations.iteritems():
    entry = Entry.objects.get(id=relation[0])
    entry.tags = ", ".join([tags[id] for id in relation[1]])
    entry.save()

cur.execute("drop table blog_entry_tags")
cur.execute("drop table tags_tag")
