from django import forms
from pagedown.widgets import PagedownWidget
from .models import Subject
from accounts.models import Profile
from django.forms import CharField
from schools.models import *
from constants import *

class SubjectForm(forms.ModelForm):
    title = forms.CharField(label='Название',required=False)
    content = forms.CharField(label='Описание', required=False)
    cost = forms.IntegerField(label='Цена', required=False)
    class Meta:
        model = Subject
        fields = [      
            "title",
            "cost",
            "content",
        ]

class SubjectForm2(forms.ModelForm):
    image_banner = forms.FileField(label='Баннер', required=False)
    image_icon = forms.FileField(label='Иконка', required=False)
    image_back = forms.FileField(label='Обои', required=False)
    color_back = forms.CharField(label='Цвет фона', required=False)
    class Meta:
        model = Subject
        fields = [      
            "image_banner",
            "image_icon",
            "image_back",
            "color_back",
        ]