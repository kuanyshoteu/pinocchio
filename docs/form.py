from django import forms
from pagedown.widgets import PagedownWidget
from docs.models import *
from django.forms import CharField

class CommentForm(forms.ModelForm):
    content = forms.CharField(label='', required = True, widget=forms.TextInput(attrs={'placeholder': 'Написать комментарий...'}))
    ffile = forms.FileField(label='Файл',required=False)
    image = forms.FileField(label='Картинка',required=False)
    class Meta:
        model = Comment
        fields = [
            "content",
            "ffile",
        ]

class DescriptionForm(forms.ModelForm):
    description = forms.CharField(label='', required=True)
    class Meta:
        model = Card
        fields = ('description', )

class FileForm(forms.ModelForm):
    file = forms.FileField(label='Файл', required=True)
    class Meta:
        model = Card
        fields = ('file', )

class CardUserForm(forms.Form):
    g_name = forms.CharField(label='', required=False)

class CardMetkaForm(forms.Form):
    g_name = forms.CharField(label='', required=False)