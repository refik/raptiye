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

"""
Includes some messages like successfull
registration, activation etc..
"""

def set_user_message(request, message):
	from raptiye.extra.session_data import create_data
	create_data(request, "message", message)

# FIXME: Break the following messages into categories

ENTRIES_ON_DATE = u"bu tarihte yazılmış yazıları görmek için tıklayın.."

COMMENTS_WARNING = u'Yorumunuz onaylandıktan sonra yayınlanacaktır. İlginiz için teşekkürler!'

PROFILE_SUCCESS = u"""
<h2>profiliniz güncellendi</h2>
<br>
profiliniz başarıyla güncellendi.. e-posta adresinizi değiştirdiyseniz yeni adresinize gelecek bağlantıya tıklayarak üyeliğinizi aktif hale getirebilirsiniz..
"""

PROFILE_ACCOUNT_ERROR = u"""
<h2>geçersiz profil</h2>
<br>
profilinize ulaşmak için öncelikle sisteme giriş yapmış olduğunuzdan emin olun.. ya da belki böyle bir profil yoktur? :)
"""

REG_SUCCESS = u"""
<h2>kaydınız başarıyla tamamlandı!</h2>
<br>
Kaydınız başarıyla alınmıştır. Az sonra kayıt sırasında kullandığınız e-posta adresine gelecek olan onay e-posta'sı içerisindeki aktivasyon bağlantısına tıklayarak üyeliğinizi aktif hale getirebilir, raptiye üzerindeki yazılara yorum yapabilirsiniz.
<br><br>
İlginiz için teşekkürler..!
"""

ACTIVATION_SUCCESS = u"""
<h2>hesabınız artık aktif!</h2>
<br>
Kullanıcı hesabınız başarıyla aktive edildi. Artık raptiye'deki yazılara yorum bırakabilir, raptiye'yle ilgili duyuruları alabilirsiniz.
<br><br>
İlginiz için teşekkürler..!
"""

ACTIVATION_ERROR = u"""
<h2>aktivasyon hatası</h2>
<br>
%s
<br><br>
İlginiz için teşekkürler..!
"""

REGISTER_SUBJECT = u"yeni kullanıcı kaydı"
REGISTER_BODY = u"""
Merhaba,

Bu e-posta'yı %s'ye yaptığınız yeni üyelik başvurusu sebebiyle alıyorsunuz. 
Üyelik başvurusunun son adımı olan aktivasyonu tamamlamak için aşağıdaki 
bağlantıya tıklayabilir ya da direk olarak tarayıcınıza yapıştırabilirsiniz.

http://%s/users/%s/activate/%s/

Üyelik başvurusunu siz yapmadıysanız bu e-posta'yı görmezden gelebilirsiniz; 
%s'den başka mesaj almanız söz konusu değildir. Söz konusu hesap, üç gün 
içinde aktivasyon gerçekleşmemesi durumunda geçersiz olacaktır.

raptiye aktivasyon bekçisi
"""

ALREADY_REGISTERED_USER = u"Kayıtlı kullanıcı adı ya da e-posta adresi.. Lütfen başka bir kullanıcı adı ya da e-posta adresi seçin."
WRONG_CAPTCHA = u"Captcha hatalı ya da girilmemiş.."

ALREADY_ACTIVE = u"Hesabını aktive etmeye çalıştığınız kullanıcı zaten aktif ya da kullandığınız aktivasyon kodu geçersiz.."
ACTIVE_NONUSER = u"Hesabını aktive etmeye çalıştığınız kullanıcı adı ya da kullandığınız aktivasyon kodu hatalı.."
INVALID_ACTIVATION_CODE = u"Kullandığınız aktivasyon kodu geçersiz ya da hatalı.."
ACTIVATION_SUBJECT = u"kullanıcı adınıza yeni e-posta adresi tanımlandı"
ACTIVATION_BODY = u"""
Merhaba,

Bu e-posta'yı %s'deki kullanıcı hesabınıza ait e-posta adresi değiştiği için
alıyorsunuz. Değişen e-posta adresinizi onaylamak için aşağıdaki bağlantıya
tıklayabilirsiniz. Eğer bu değişikliği siz yapmadıysanız lütfen bilgi@raptiye.org
adresine bir e-posta gönderin.

http://%s/users/%s/activate/%s/

Söz konusu hesabınız, üç gün içinde aktivasyon gerçekleşmemesi durumunda geçersiz 
olacaktır.

raptiye aktivasyon bekçisi
"""

TAGS_SUCCESS = u"%s ile etiketlenmiş yazılar (%d) görüntüleniyor.."

TAGS_ERROR = u"""
<h2>etiket hatalı mı ne?</h2>
<br>
aradığınız etikete şu anda ulaşılamıyor.. etiket kapalı ya da kapsama alanı dışında..
"""

POLL_ERROR = u"Anket oylamasında hata oluştu! Lütfen daha sonra tekrar deneyin.."

LOGIN_ERROR = u"Kullanıcı Adı ya da Şifre hatalı.. Lütfen tekrar deneyin.."

ACCOUNT_NEEDS_ACTIVATION = u"Kullanıcı hesabınızı aktifleştirmeden kullanamazsınız."

NEW_COMMENT_SUBJECT = u"yeni yorum var!"
NEW_COMMENT_BODY = u"""Merhaba,

Bu e-posta'yı \"%s\" adlı yazıya yapılan yeni ve henüz onaylanmamış (taze!)
yorumdan haberdar olmak için alıyorsun! O halde durma; hemen aşağıdaki
bağlantıya tıklayarak yorumu gör ve onayla!

%s

Sevgilerle..

raptiye yorum bekçisi
"""

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

OPENID_DISCOVERY_FAILURE = u"openid adresiniz tanımlanamadı.. lütfen doğru bir adres girdiğinizden emin olun."
OPENID_FAILURE_MESSAGE = u"openid adresiniz ile girişte bir hata oluştu. lütfen daha sonra tekrar deneyin."
OPENID_EXISTING_USERNAME = u"seçtiğiniz kullanıcı adı kullanılıyor.. lütfen başka bir kullanıcı adıyla tekrar deneyin."
OPENID_AUTH_FAILURE = u"openid adresinizle raptiye'ye girişte bir sorun oluştu.. lütfen daha sonra tekrar deneyin."
OPENID_PROVIDER_FAILED = u"openid sağlayıcınızdan gelen veride bir sorun var. lütfen başka bir sağlayıcıyla deneyin."

FORGOTTEN_PASSWORD_SUBJECT = u"yeni raptiye şifreniz"
FRG_CANNOT_FIND_EMAIL = u"raptiye'de kayıtlı böyle bir e-posta adresi bulunmuyor."
FORGOTTEN_PASSWORD_BODY = u"""
Merhaba,

Bu e-posta'yı %s'deki kullanıcı hesabınıza ait şifreyi değiştirmek istediğiniz 
için alıyorsunuz. Aşağıdaki yeni şifrenizle birlikte %s'deki hesabınıza giriş 
yapabilirsiniz. Hesabınıza giriş yaptıktan sonra profil ayarlarınızdan şifrenizi 
kolayca hatırlayabileceğiniz daha zor bir şifre ile değiştirmeniz hesabınızın 
güvenliği açısından gereklidir.

Yeni şifreniz: %s

raptiye şifre bekçisi
"""

SEARCH_BODY = u"<strong><i>%s</i></strong> %s içeren yazılar (%d) görüntüleniyor.."
SEARCH_WORD = u"kelimesini"
SEARCH_WORD_PLURAL = u"kelimelerini"

SEARCH_FAILED = u"""
<h2>arama başarısız</h2>
<br>
geçersiz bir arama yaptınız.. eğer sağdaki kutuyu kullandığınız halde bu mesajı görüyorsanız site büyük ihtimalle patlamış.. :) durumu bana bildirebilirseniz düzeltmeye çalışırım.. ilginiz için teşekkürler!
"""

SEARCH_NO_ITEM = u"""
<h2>yok böyle bir şey?</h2>
<br>
raptiye'de olmayan bir şeyi arattınız.. demek ki hala üzerine bir şeyler yazmadığım konular var.. :)
"""

ENTRIES_FOR_DAY = u"%s.%s.%s tarihinde yazılmış yazılar görüntüleniyor.."

COMMENT_FORM_FULLNAME = u"Ad Soyad"
COMMENT_FORM_EMAIL = u"E-Posta"
COMMENT_FORM_WEBSITE = u"Web Sitesi"
COMMENT_FORM_COMMENT = u"Yorum"
COMMENT_FORM_CAPTCHA = u"Captcha"
COMMENT_FORM_NOTIFICATION = u"Bu yazıdaki değişikliklerden beni haberdar et"
COMMENT_FORM_INVALID_FULLNAME = u"isim hatalı"
COMMENT_FORM_INVALID_CAPTCHA = u"captcha hatalı"

CAPTCHA_FAILURE = u"captcha hatalı"
OPERATION_FAILURE = u"işlem başarısız.."
INVALID_FORM_FIELD = u"%s hatalı"
MISSING_INFORMATION = u"bilgiler eksik"
COMMENT_SENT = u"yorumunuz gönderildi.."
LOGIN_NEEDED = u"giriş yapılmamış"

USERS_FORM_USERNAME = u"Kullanıcı Adı"
USERS_FORM_PASSWORD = u"Şifre"
USERS_FORM_INVALID_USERNAME = u"Kullanıcı ismi yalnızca harf ve rakamlardan oluşabilir."
USERS_FORM_NAME = u"Ad"
USERS_FORM_SURNAME = u"Soyad"
USERS_FORM_EMAIL = u"E-Posta"
USERS_FORM_INVALID_NAME = u"İsim alanı yalnızca harfler ve boşluklardan oluşabilir."
USERS_FORM_INVALID_SURNAME = u"Soyadı alanı yalnızca harflerden oluşabilir."
USERS_FORM_AVATAR = u"Avatar"
USERS_FORM_WEBSITE = u"Web Sitesi"
USERS_FORM_OPENID = u"OpenID"

DJANGO_NOT_FOUND = u"""[ERROR] django cannot be found.

Please install django on your system and make sure it's available
in your PYTHONPATH.

You can also put django and raptiye in the same folder and add that
folder into your PYTHONPATH.
"""

SETTINGS_NOT_FOUND = u"""[WARNING] settings.py cannot be found. Creating one for you...

Depending on the dependencies installed on your computer, raptiye will now create
a default settings.py for you. You can then review and make changes on it to enable
or disable various features.

You'll especially have to fill the details in ADMIN_SETTINGS section to get mailing
to the users (for several reasons) work.

"""

PIL_NOT_FOUND = u"""[ERROR] PIL library not found.

PIL (Python Imaging Library) is a requirement for raptiye in order to make 
ImageFields work. Please install the library and try again.
"""

POSTGRESQL_NOT_FOUND = u"""[ERROR] PostgreSQL database backend not found.

Please install PostgreSQL binding for Python and try again.
"""

POSTGRESQL2_NOT_FOUND = u"""[ERROR] PostgreSQL2 database backend not found.

Please install Postgresql2 binding for Python and try again.
"""

MYSQL_NOT_FOUND = u"""[ERROR] MySQL database backend not found.

Please install MySQL binding for Python and try again.
"""

ORACLE_NOT_FOUND = u"""[ERROR] Oracle database backend not found.

Please install Oracle binding for Python and try again.
"""

INVALID_DB_BACKEND = u"""[ERROR] Invalid database backend.

You have specified an invalid database backend in your settings.
You can refer to Django Documentation for available choices and
try again.
"""