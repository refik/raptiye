#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from os import path
from django.conf import settings
from captcha import Captcha

c = Captcha("/home/tunix/Desktop")
text = c.generate_random_text()
print "text generated for captcha: " + text
c.set_filename(text + ".jpg")
c.set_text(text)
c.set_size(120, 50)
c.set_fg_color("black")
c.set_bg_color("white")
c.set_font(path.join(settings.MEDIA_ROOT, "fonts", "astonish.ttf"), 40)
c.generate_captcha()

