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

class LoginForm(forms.Form):
	username = forms.CharField(label=u"Kullanıcı Adı", widget=forms.TextInput(attrs={"autocomplete": "off"}))
	password = forms.CharField(label=u"Şifre", widget=forms.PasswordInput(attrs={"autocomplete": "off"}))
	
	def clean_username(self):
		u"A username must include only ASCII characters and numbers.."
		pattern = re.compile(u"[^a-zA-Z0-9]")
		if pattern.search(self.cleaned_data["username"]):
			raise forms.ValidationError(u"Kullanıcı ismi yalnızca harf ve rakamlardan oluşabilir.")
		return self.cleaned_data["username"]

class RegistrationForm(LoginForm):
	name = forms.CharField(label=u"Ad", min_length=2, max_length=30, widget=forms.TextInput(attrs={"autocomplete": "off"}), required=False)
	surname = forms.CharField(label=u"Soyad", min_length=2, max_length=30, widget=forms.TextInput(attrs={"autocomplete": "off"}), required=False)
	email = forms.EmailField(label=u"E-Posta", widget=forms.TextInput(attrs={"autocomplete": "off"}))
	
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
	# subclassing other forms but overwriting their attrs..
	username = forms.CharField(label=u"Kullanıcı Adı", max_length=30, widget=forms.HiddenInput)
	password = forms.CharField(label=u"Şifre", widget=forms.PasswordInput(attrs={"autocomplete": "off"}), required=False)
	avatar = forms.URLField(label=u"Avatar", required=False, verify_exists=True, widget=forms.TextInput(attrs={"autocomplete": "off"}))
	website = forms.URLField(label=u"Web Sitesi", required=False, verify_exists=True, widget=forms.TextInput(attrs={"autocomplete": "off"}))

class ForgottenPasswordForm(forms.Form):
	email = forms.EmailField(label=u"E-Posta", widget=forms.TextInput(attrs={"autocomplete": "off"}))

class OpenIDForm(forms.Form):
	attrs = {
		"autocomplete": "off",
		"value": "http://",
	}
	identifier = forms.URLField(label=u"Kimlik", widget=forms.TextInput(attrs))