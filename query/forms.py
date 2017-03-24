from django import forms
from django.utils.encoding import python_2_unicode_compatible

@python_2_unicode_compatible
class Keywords(forms.Form):
    keywords = forms.CharField(label="keywords",max_length=200)
    def __str__(self):
        return self.keywords_text
