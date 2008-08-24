#-*- encoding: utf-8 -*-

import re
from django import forms

class LoginForm(forms.Form):
	username = forms.CharField(label=u"Kullanıcı Adı")
	password = forms.CharField(label=u"Şifre", widget=forms.PasswordInput)

class RegistrationForm(LoginForm):
	name = forms.CharField(label=u"Ad", min_length=2, max_length=30)
	surname = forms.CharField(label=u"Soyad", min_length=2, max_length=30)
	email = forms.EmailField(label=u"E-Posta")
	
	def clean_name(self):
		u"A name must only have a combination of a-zA-Z, Turkish chars. and space."
		pattern = re.compile(u"[^a-zA-ZıöçşğüİÖÇŞĞÜ ]")
		if pattern.search(self.cleaned_data["name"]):
			raise forms.ValidationError(u"İsim alanı yalnızca harfler ve boşluklardan oluşabilir.")
		return self.cleaned_data["name"]
			
	def clean_surname(self):
		u"A surname must only have a combination of a-zA-Z and Turkish characters."
		pattern = re.compile(u"[^a-zA-ZıöçşğüİÖÇŞĞÜ]")
		if pattern.search(self.cleaned_data["surname"]):
			raise forms.ValidationError(u"Soyadı alanı yalnızca harflerden oluşabilir.")
		return self.cleaned_data["surname"]
	
class ProfileForm(RegistrationForm):
	username = forms.CharField(label=u"Kullanıcı Adı", max_length=30, widget=forms.HiddenInput)
	avatar = forms.URLField(label=u"Avatar", required=False, verify_exists=True)
	website = forms.URLField(label=u"Web Sitesi", required=False, verify_exists=True)