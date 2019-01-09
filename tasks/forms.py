from django import forms
from pagedown.widgets import PagedownWidget
from .models import Task
from django.forms import CharField


class TaskForm(forms.ModelForm):
    text = forms.CharField(label='Условие', widget=forms.Textarea(attrs={'rows':1, 'cols':60}), required=False)
    answer = forms.CharField(label='Ответ', widget=forms.Textarea(attrs={'rows':1, 'cols':4}), required=True)
    image = forms.FileField(label='',required=False)
    class Meta:
        model = Task
        fields = [
            "text",
            "image",
            "answer",
        ]

class AnswerForm(forms.Form):
    answerr = forms.CharField(label='', widget=forms.Textarea(attrs={'rows':1, 'cols':4}), required=False)
    
class TexttForm(forms.Form):
    textt = forms.CharField(label='', widget=forms.Textarea(attrs={'rows':1, 'cols':60}), required=False)
