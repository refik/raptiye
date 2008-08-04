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

MSG['tr']['ENTRIES_ON_DATE'] = u"<strong>%s.%s.%s</strong> tarihinde yazılmış yazılar görüntüleniyor.."

MSG['en']['ENTRIES_ON_DATE'] = u"entries written on <strong>%s.%s.%s</strong> are shown.."

MSG['tr']['SEARCH_SUCCESS'] = u"<strong><i>%s</i></strong> %s içeren yazılar (%d) görüntüleniyor.."

MSG['en']['SEARCH_SUCCESS'] = u"entries which contain <strong><i>%s</i></strong> as the %s. (found: %s)"

MSG['tr']['SEARCH_KEYWORD'] = u"kelimesini"

MSG['en']['SEARCH_KEYWORD'] = u"keyword"

MSG['tr']['SEARCH_KEYWORD_PLURAL'] = u"kelimelerini"

MSG['en']['SEARCH_KEYWORD_PLURAL'] = u"keywords"

MSG['tr']['SEARCH_NO_ITEM'] = u"""
<h2>yok böyle bir şey?</h2>
<br>
raptiye'de olmayan bir şeyi arattınız.. demek ki hala üzerine bir şeyler yazmadığım konular var.. :)
"""

MSG['en']['SEARCH_NO_ITEM'] = u"""
<h2>nothing found</h2>
<br>
at last you've searched for something i haven't written about.. :) cool!
"""

MSG['tr']['PROFILE_SUCCESS'] = u"""
<h2>profiliniz güncellendi</h2>
<br>
profiliniz başarıyla güncellendi.. e-posta adresinizi değiştirdiyseniz yeni adresinize gelecek bağlantıya tıklayarak üyeliğinizi aktif hale getirebilirsiniz..
"""

MSG['en']['PROFILE_SUCCESS'] = u"""
<h2>profile updated</h2>
<br>
your profile is updated successfully! if you've updated your e-mail address, please click the link in the e-mail we've just sent to your new e-mail address..
"""

MSG['tr']['PROFILE_ACCOUNT_ERROR'] = u"""
<h2>geçersiz profil</h2>
<br>
profilinize ulaşmak için öncelikle sisteme giriş yapmış olduğunuzdan emin olun.. ya da belki böyle bir profil yoktur? :)
"""

MSG['en']['PROFILE_ACCOUNT_ERROR'] = u"""
<h2>invalid profile</h2>
<br>
have you logged in before trying to reach your profile? never mind.. maybe there's no profile like this.. :)
"""

MSG['tr']['REG_SUCCESS'] = u"""
<h2>kaydınız başarıyla tamamlandı!</h2>
<br>
Kaydınız başarıyla alınmıştır. Az sonra kayıt sırasında kullandığınız e-posta adresine gelecek olan onay e-posta'sı içerisindeki aktivasyon bağlantısına tıklayarak üyeliğinizi aktif hale getirebilir, raptiye üzerindeki yazılara yorum yapabilirsiniz.
<br><br>
İlginiz için teşekkürler..!
"""

MSG['en']['REG_SUCCESS'] = u"""
<h2>registration successfull!</h2>
<br>
you've successfully registered! You can now click on the activation link that has just been sent to you to comment on the blog entries on raptiye..
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

MSG['en']['ACTIVATION_SUCCESS'] = u"""
<h2>your account is now enabled!</h2>
<br>
your account on raptiye is now successfully enabled! you can now comment on blog entries and can be notified about the entries you want..
<br><br>
thanks for your attention!
"""

MSG['tr']['ACTIVATION_ERROR'] = u"""
<h2>%s</h2>
<br>
%s
<br><br>
İlginiz için teşekkürler..!
"""

MSG['en']['ACTIVATION_ERROR'] = u"""
<h2>%s</h2>
<br>
%s
<br><br>
thanks for your attention!
"""

MSG['tr']['TAGS_SUCCESS'] = u"<strong>%s</strong> ile etiketlenmiş yazılar (%d) görüntüleniyor.."

MSG['en']['TAGS_SUCCESS'] = u"entries that are tagged with <strong>%s</strong> are shown.. (found: %d)"

MSG['tr']['TAGS_ERROR'] = u"""
<h2>etiket hatalı mı ne?</h2>
<br>
aradığınız etikete şu anda ulaşılamıyor.. etiket kapalı ya da kapsama alanı dışında..
"""

MSG['en']['TAGS_ERROR'] = u"""
<h2>missing or wrong tag..</h2>
<br>
the tag you're trying to reach cannot be reached at the moment.. please try again later..
"""