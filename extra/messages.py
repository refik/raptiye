#-*- encoding: utf-8 -*-

"""
Includes some messages like successfull
registration, activation etc..
"""

# All messages are stored in this dictionary..
MSG = {}
# All Turkish messages are stored in this subdictionary..
MSG['tr'] = {}
# All English messages are stored in this subdictionary..
MSG['en'] = {}

MSG['tr']['ENTRIES_ON_DATE'] = u"%s.%s.%s tarihinde yazılmış yazılar görüntüleniyor.."

MSG['tr']['SEARCH_FAILED'] = u"""
<h2>arama başarısız</h2>
<br>
geçersiz bir arama yaptınız.. eğer sağdaki kutuyu kullandığınız halde bu mesajı görüyorsanız lütfen site büyük ihtimalle patlamış.. :) durumu bana bildirebilirseniz düzeltmeye çalışırım.. ilginiz için teşekkürler!
"""

MSG['tr']['SEARCH_NO_ITEM'] = u"""
<h2>yok böyle bir şey?</h2>
<br>
raptiye'de olmayan bir şeyi arattınız.. demek ki hala üzerine bir şeyler yazmadığım konular var.. :)
"""

MSG['tr']['PROFILE_SUCCESS'] = u"""
<h2>profiliniz güncellendi</h2>
<br>
profiliniz başarıyla güncellendi.. e-posta adresinizi değiştirdiyseniz yeni adresinize gelecek bağlantıya tıklayarak üyeliğinizi aktif hale getirebilirsiniz..
"""

MSG['tr']['PROFILE_ACCOUNT_ERROR'] = u"""
<h2>geçersiz profil</h2>
<br>
profilinize ulaşmak için öncelikle sisteme giriş yapmış olduğunuzdan emin olun.. ya da belki böyle bir profil yoktur? :)
"""

MSG['tr']['REG_SUCCESS'] = u"""
<h2>kaydınız başarıyla tamamlandı!</h2>
<br>
Kaydınız başarıyla alınmıştır. Az sonra kayıt sırasında kullandığınız e-posta adresine gelecek olan onay e-posta'sı içerisindeki aktivasyon bağlantısına tıklayarak üyeliğinizi aktif hale getirebilir, raptiye üzerindeki yazılara yorum yapabilirsiniz.
<br><br>
İlginiz için teşekkürler..!
"""

MSG['tr']['ACTIVATION_SUCCESS'] = u"""
<h2>hesabınız artık aktif!</h2>
<br>
Kullanıcı hesabınız başarıyla aktive edildi. Artık raptiye'deki yazılara yorum bırakabilir, raptiye'yle ilgili duyuruları alabilirsiniz.
<br><br>
İlginiz için teşekkürler..!
"""

MSG['tr']['ACTIVATION_ERROR'] = u"""
<h2>%s</h2>
<br>
%s
<br><br>
İlginiz için teşekkürler..!
"""

MSG['tr']['TAGS_SUCCESS'] = u"%s ile etiketlenmiş yazılar (%d) görüntüleniyor.."

MSG['tr']['TAGS_ERROR'] = u"""
<h2>%s</h2>
<br>
%s
"""