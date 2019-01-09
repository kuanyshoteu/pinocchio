from django import forms
from pagedown.widgets import PagedownWidget
from .models import Squad
from accounts.models import Profile
from django.forms import CharField


class SquadForm(forms.ModelForm):
    title = forms.CharField(label='Название')
    cabinet = forms.CharField(label='Кабинет',required=False)
    content = forms.CharField(label='Описание',required=False)
    slogan = forms.CharField(label='Краткое описание',required=False)
    image_banner = forms.FileField(label='Большая картинка',required=False)
    image_icon = forms.FileField(label='Иконка',required=False)
    
    class Meta:
        model = Squad
        fields = [      
            "title",
            "content",
            "image_banner",
            "image_icon",
            "cabinet",
        ]