from django import forms
from pagedown.widgets import PagedownWidget
from .models import School
from accounts.models import Profile
from django.forms import CharField


class SchoolForm(forms.ModelForm):
    title = forms.CharField(label='Название')
    content = forms.CharField(label='Описание',required=False)
    address = forms.CharField(label='Адрес',required=False)
    image_banner = forms.FileField(label='Большая картинка',required=False)
    image_icon = forms.FileField(label='Иконка',required=False)
    
    class Meta:
        model = School
        fields = [      
            "title",
            "content",
            "address",
            "image_banner",
            "image_icon",
        ]