#-*- encoding: utf-8 -*-

from django import newforms as forms

class LoginForm(forms.Form):
	username = forms.CharField(label="Kullanıcı Adı")
	password = forms.CharField(label="Şifre", widget=forms.PasswordInput)

class RegistrationForm(LoginForm):
	name = forms.CharField(label=u"Ad")
	surname = forms.CharField(label=u"Soyad")
	email = forms.EmailField(label=u"E-Posta")
	
class ProfileForm(RegistrationForm):
	username = forms.CharField(label="Kullanıcı Adı", widget=forms.HiddenInput)
	avatar = forms.CharField(label=u"Avatar", required=False)
	website = forms.URLField(label=u"Web Sitesi", required=False)
