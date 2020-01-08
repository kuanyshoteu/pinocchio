from django import forms
from pagedown.widgets import PagedownWidget
from .models import Profile, MissLesson
from django.forms import CharField
from django.db.models import Q
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
    )

class ProfileForm(forms.ModelForm):
    image = forms.FileField(label = 'Ава', required = False)
    phone = forms.CharField(label='Телефон',required=True)
    mail = forms.CharField(label='Почта',required=False)
    class Meta:
        model = Profile
        fields = [
            "image",
            "phone",
            "mail",
        ]

class MissLessonForm(forms.ModelForm):
    text = forms.CharField(label='Причина',required=True)
    image = forms.FileField(label = 'Справка', required = False)
    class Meta:
        model = MissLesson
        fields = [
            "text",
            "image",
        ]

class EmptyForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
        ]
