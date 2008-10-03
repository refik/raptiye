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

import re
from django import forms

class CommentForm(forms.Form):
	anonymous_full_name = forms.CharField(label=u"Ad Soyad", max_length=100)
	anonymous_email = forms.EmailField(label=u"E-Posta", max_length=100)
	anonymous_website = forms.URLField(label=u"Web Sitesi", required=False, verify_exists=True, max_length=100)
	comment_body = forms.CharField(label=u"Yorum")
	captcha = forms.CharField(label=u"Captcha", max_length=6, widget=forms.TextInput(attrs={"size": "6"}))
	notification = forms.BooleanField(label=u"Bu yazıdaki değişikliklerden beni haberdar et", required=False)
	
	def clean_anonymous_full_name(self):
		u"A name must only have a combination of a-zA-Z, Turkish chars. and space."
		pattern = re.compile(u"[^a-zA-ZıöçşğüİÖÇŞĞÜ ]")
		if pattern.search(self.cleaned_data["anonymous_full_name"]):
			raise forms.ValidationError(u"isim hatalı")
		return self.cleaned_data["anonymous_full_name"]
	
	def clean_captcha(self):
		u"A captcha can only have ASCII characters and digits."
		pattern = re.compile(u"[^a-zA-Z0-9]")
		if pattern.search(self.cleaned_data["captcha"]):
			raise forms.ValidationError(u"captcha hatalı")
		return self.cleaned_data["captcha"]