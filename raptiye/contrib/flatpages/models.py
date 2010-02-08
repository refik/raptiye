#-*- coding: utf-8 -*-

from django.db import models
from django.conf import settings
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _

class FlatPage(models.Model):
    url = models.CharField(_('URL'), max_length=100, db_index=True)
    title = models.CharField(_('title'), max_length=200)
    content = models.TextField(_('content'), blank=True)
    # TODO: implement comments for flatpages
    enable_comments = models.BooleanField(_('enable comments'))
    template_name = models.CharField(_('template name'), max_length=70, blank=True, default="blog/flatpage.html")
    registration_required = models.BooleanField(_('registration required'), help_text=_("If this is checked, only logged-in users will be able to view the page."))
    sites = models.ManyToManyField(Site)
    # FIXME: what if LANGUAGES isn't in settings.py?
    lang = models.CharField(_(u"Language"), choices=settings.LANGUAGES, max_length=2, default="tr")
    show_on_homepage = models.BooleanField(_("Show on HomePage"), default=False)

    class Meta:
        verbose_name = _('flat page')
        verbose_name_plural = _('flat pages')
        ordering = ('url',)

    def __unicode__(self):
        return u"%s -- %s" % (self.url, self.title)

    def get_absolute_url(self):
        return self.url

    def show_flag(self):
        # FIXME: the url bounds this package to raptiye
        return "<img src='%s%s%s.png' alt='%s' style='display: block; margin: 0 auto;'>" % (settings.MEDIA_URL, "default/images/", self.lang, _(u"flag of language"))

    show_flag.short_description = _(u"Flag of Language")
    show_flag.allow_tags = True

