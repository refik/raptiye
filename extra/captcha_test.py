#!/usr/bin/env python
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