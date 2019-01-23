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

class SubthemeTextForm(forms.ModelForm):
    content = forms.CharField(label='', widget=PagedownWidget(show_preview = False), required=True)    
    class Meta:
        model = Subtheme
        fields = [
            "content",
        ]

class SubthemeFileForm(forms.ModelForm):
    file = forms.FileField(label='', required=True) 
    class Meta:
        model = Subtheme
        fields = [
            "file",
        ]
class SubthemeVideoForm(forms.ModelForm):
    youtube_video_link = forms.CharField(label='Ссылка на видео:', required=False)
    video = forms.FileField(label='Загрузите свое видео:', required=False)    
    class Meta:
        model = Subtheme
        fields = [
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

