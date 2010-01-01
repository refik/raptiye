from django import forms
from django.forms import ValidationError
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from flatpages.models import FlatPage

class FlatpageForm(forms.ModelForm):
    url = forms.RegexField(label=_("URL"), max_length=100, regex=r'^[-\w/]+$',
        help_text = _("Example: '/about/contact/'. Make sure to have leading"
            " and trailing slashes."),
        error_message = _("This value must contain only letters, numbers,"
            " underscores, dashes or slashes."))
    content = forms.CharField(widget=forms.Textarea(attrs={"style": "width: 900px; height: 600px"}))

    def clean_url(self):
        """
        Checks if url has trailing slash and raises 
        ValidationError if not..

        """
        
        data = self.cleaned_data["url"]
        
        if data[-1] != "/":
            raise ValidationError(_(u"You should add a trailing slash at the end of the url."))
        
        return data

    class Meta:
        model = FlatPage

class FlatPageAdmin(admin.ModelAdmin):
    form = FlatpageForm
    fieldsets = (
        (None, {'fields': ('url', 'title', 'content', 'sites', 'lang', 'show_on_homepage')}),
        (_('Advanced options'), {'classes': ('collapse',), 'fields': ('enable_comments', 'registration_required', 'template_name')}),
    )
    list_display = ('url', 'title', 'show_flag', 'show_on_homepage')
    list_filter = ('sites', 'enable_comments', 'registration_required', 'lang', 'show_on_homepage')
    search_fields = ('url', 'title')

    class Media:
        # js = ("common/fckeditor/fckeditor.js", "common/fckeditor_inclusion.js")
        pass

admin.site.register(FlatPage, FlatPageAdmin)

