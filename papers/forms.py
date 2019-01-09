from django import forms
from pagedown.widgets import PagedownWidget
from .models import *
from django.forms import CharField, BooleanField


class PaperForm(forms.ModelForm):
    title = forms.CharField(label='Заголовок:', widget=forms.Textarea(attrs={'rows':1, 'cols':30}))
    content = forms.CharField(label='Описание:', widget=PagedownWidget(show_preview = False), required=False)
    is_homework = forms.BooleanField(label='Сделать домашним заданием',initial=False, required=False, widget = forms.CheckboxInput(attrs={'class': 'ui toggle checkbox'}))
    class Meta:
        model = Paper
        fields = [
            "title",
            'is_homework',            
            "content",
        ]

class SubthemeForm(forms.ModelForm):
    title = forms.CharField(label='<b>Название подраздела:', widget=forms.Textarea(attrs={'rows':1, 'cols':30}))
    content = forms.CharField(label='Текст в подразделе:', widget=PagedownWidget(show_preview = False), required=False)
    file = forms.FileField(label='Загрузите дополнительный файл:', required=False)
    youtube_video_link = forms.CharField(label='Ссылка на видео:', required=False)
    video = forms.FileField(label='Загрузите свое видео:', required=False)
    
    class Meta:
        model = Subtheme
        fields = [
            "title",     
            "content",
            "file",
            "youtube_video_link",
            "video",
        ]

class CourseForm(forms.ModelForm):
    title = forms.CharField(label='',required=False)
    content = forms.CharField(label='', widget=PagedownWidget(show_preview = False), required=False)
    cost = forms.IntegerField(label='', required=False)
    image = forms.FileField(label='',required=False)
    
    class Meta:
        model = Course
        fields = [      
            "title",
            "image",
            "content",
            "cost",
        ]

