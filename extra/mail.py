#-*- encoding: utf-8 -*-

from django.conf import settings

COMMENT_NOTIFICATION_SUBJECT = u"yorum bekçisinden haberiniz var!"

COMMENT_NOTIFICATION_MESSAGE = u"""
Merhaba,

Bu e-posta'yı \"%s\" adlı yazıya yeni bir yorum yazıldığı için alıyorsunuz. İlgili 
yazıya ait yorumlardan artık haberdar olmak istemiyorsanız profil ayarlarını 
ziyaret etmenizde fayda var. Yazılanları okumak için aşağıdaki adrese 
tıklayabilirsiniz.

%s

raptiye yorum bekçisi
"""

REGISTER_SUBJECT = settings.EMAIL_SUBJECT_PREFIX + u"yeni kullanıcı kaydı"
REGISTER_BODY = u"""
Merhaba,

Bu e-posta'yı %s'ye yaptığınız yeni üyelik başvurusu sebebiyle alıyorsunuz. 
Üyelik başvurusunun son adımı olan aktivasyonu tamamlamak için aşağıdaki 
bağlantıya tıklayabilir ya da direk olarak tarayıcınıza yapıştırabilirsiniz.

http://%s/users/%s/activate/%s/

Üyelik başvurusunu siz yapmadıysanız bu e-posta'yı görmezden gelebilirsiniz; 
%s'den başka mesaj almanız söz konusu değildir. Söz konusu hesap, üç gün 
içinde aktivasyon gerçekleşmemesi durumunda geçersiz olacaktır.

"""

ACTIVATION_SUBJECT = settings.EMAIL_SUBJECT_PREFIX + u"kullanıcı adınıza yeni e-posta adresi tanımlandı"
ACTIVATION_BODY = u"""
Merhaba,

Bu e-posta'yı %s'deki kullanıcı hesabınıza ait e-posta adresi değiştiği için
alıyorsunuz. Değişen e-posta adresinizi onaylamak için aşağıdaki bağlantıya
tıklayabilirsiniz. Eğer bu değişikliği siz yapmadıysanız lütfen bilgi@raptiye.org
adresine bir e-posta gönderin.

http://%s/users/%s/activate/%s/

Söz konusu hesabınız, üç gün içinde aktivasyon gerçekleşmemesi durumunda geçersiz 
olacaktır.

"""

def send_comment_notification(entry):
	from django.core.mail import send_mass_mail
	
	messages = [(COMMENT_NOTIFICATION_SUBJECT, COMMENT_NOTIFICATION_MESSAGE % (entry.title, entry.get_full_url()),
		settings.EMAIL_INFO_ADDRESS_TR, [comment.author.email])
		for comment in entry.comments.filter(notification=True)]
	
	send_mass_mail(messages, settings.EMAIL_FAIL_SILENCE)

def create_activation_key():
	from random import sample
	import sha, string
	choices = list(string.letters + string.digits)
	return sha.new(settings.SECRET_KEY[:20] + "".join(sample(choices, 5))).hexdigest()
