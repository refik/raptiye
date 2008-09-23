#-*- encoding: utf-8 -*-

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
		return "".join(sample(choices, self.get_text_length()))

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
		draw.text((10, 0), self.get_text(), fill=1, font=self.get_font())
		im.save(file, "JPEG")
		file.close()
