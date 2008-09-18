#-*- encoding: utf-8 -*-

import re
from django import forms

class CommentForm(forms.Form):
	anonymous_full_name = forms.CharField(label=u"Ad Soyad", required=False, max_length=100)
	anonymous_email = forms.EmailField(label=u"E-Posta", required=False, max_length=100)
	anonymous_website = forms.URLField(label=u"Web Sitesi", required=False, verify_exists=True, max_length=100)
	comment = forms.CharField(label=u"Yorum")
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