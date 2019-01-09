from django import forms
from pagedown.widgets import PagedownWidget
from .models import Squad
from django.forms import CharField


class TableChangeForm(forms.ModelForm):
    de = forms.IntegerField(widget=forms.HiddenInput)
    
    class Meta:
        model = Squad
        fields = [
            "de",
        ]