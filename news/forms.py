from django import forms
from pagedown.widgets import PagedownWidget
from .models import Post

class PostForm(forms.ModelForm):
    title = forms.CharField(label='Название')
    content = forms.CharField(label='Описание',required=False)
    image = forms.FileField(label='Большая картинка',required=False)
    
    class Meta:
        model = Post
        fields = [      
            "title",
            "content",
            "image",
        ]