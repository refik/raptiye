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

import sys

try:
	import Image, ImageDraw, ImageFont
except ImportError:
	sys.exit(0)

class Captcha:
	"""
	creates an image which consists of characters...

	default length is 6 characters.

	@requires pil
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
	fgColor = u""
	bgColor = u""

	def __init__(self, file_path="", filename="", size=None, fgColor="", bgColor=""):
		self.file_path = file_path
		self.filename = filename
		self.size = size
		self.fgColor = fgColor
		self.bgColor = bgColor
	
	def set_fg_color(self, color):
		self.fgColor = color
	
	def get_fg_color(self):
		return self.fgColor

	def set_bg_color(self, color):
		self.bgColor = color
	
	def get_bg_color(self):
		return self.bgColor
	
	def set_file_path(self, path):
		self.file_path = path
	
	def get_file_path(self):
		return self.file_path

	def generate_random_text(self):
		from random import sample
		import string
		choices = list(string.letters + string.digits)
		return u"".join(sample(choices, self.get_text_length()))

	def set_text_length(self, length=6):
		self.text_length = length
	
	def get_text_length(self):
		return self.text_length

	def set_font(self, font, size):
		self.font = ImageFont.truetype(font, size)
	
	def get_font(self):
		return self.font
	
	def set_size(self, width, height):
		self.size = (width, height)
	
	def get_size(self):
		return self.size
	
	def set_filename(self, filename):
		self.filename = filename
	
	def get_filename(self):
		return self.filename

	def set_text(self, text):
		self.text = text
	
	def get_text(self):
		return self.text
	
	def generate_hash(self, salt):
		import sha
		hash = sha.new(salt + self.get_text()).hexdigest()
		return hash

	def generate_captcha(self):
		from os import path
		file = open(path.join(self.get_file_path(), self.get_filename()), "w")
		im = Image.new("RGB", self.get_size(), self.get_bg_color())
		draw = ImageDraw.Draw(im)
		draw.text((15, 0), self.get_text(), fill=1, font=self.get_font())
		im.save(file, "JPEG")
		file.close()
