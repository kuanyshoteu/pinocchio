from django import forms
from pagedown.widgets import PagedownWidget
from .models import Subject
from accounts.models import Profile
from django.forms import CharField


class SubjectForm(forms.ModelForm):
    title = forms.CharField(label='',required=False)
    content = forms.CharField(label='', required=False)
    cabinet = forms.CharField(label='', required=False)
    image_banner = forms.FileField(label='', required=False)
    image_icon = forms.FileField(label='', required=False)
    image_back = forms.FileField(label='', required=False)
    color_back = forms.CharField(label='', required=False)
    class Meta:
        model = Subject
        fields = [      
            "title",
            "content",
            "cabinet",
            "image_banner",
            "image_icon",
            "image_back",
            "color_back"
        ]