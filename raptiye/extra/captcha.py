# coding: utf-8
# 
# raptiye
# Copyright (C) 2009  Alper KANAT <alperkanat@raptiye.org>
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
# along with this program. If not, see <http://www.gnu.org/licenses/>.
# 

from hashlib import sha1
import Image, ImageDraw, ImageFont
from os import path
from random import sample
import string
import sys

class Captcha:
    """
    creates an image which consists of characters...

    default length is 6 characters.

    @requires python-imaging
    @param file_path String that represents captcha file path
    @param filename String that represents the captcha filename
    @param size Tuple which represents width and height of captcha
    @param fgColor String for the text color of captcha
    @param bgColor String for the background color

    """

    text = u""
    text_length = 6
    file_path = u""
    filename = u""
    size = None
    font = None
    fgColor = u"black"
    bgColor = u"white"

    def __init__(self, file_path="", filename="", size=None):
        self.file_path = file_path
        self.filename = filename
        self.size = size
        self.text = self.generate_random_text(self.text_length)

    @staticmethod
    def generate_random_text(length=6):
        choices = list(string.letters + string.digits)
        return u"".join(sample(choices, length))

    def set_font(self, font, size):
        self.font = ImageFont.truetype(font, size)

    def generate_hash(self, salt):
        hash = sha1(salt + self.text).hexdigest()
        return hash

    def generate_captcha(self):
        file = open(path.join(self.file_path, self.filename), "w")
        im = Image.new("RGB", self.size, self.bgColor)
        draw = ImageDraw.Draw(im)
        draw.text((15, 0), self.text, fill=1, font=self.font)
        im.save(file, "JPEG")
        file.close()
