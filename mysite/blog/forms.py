from django import forms
from .models import Comment

class NewPostForm(forms.Form):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = forms.CharField(max_length=250)
    slug = forms.SlugField(required=True)
    author = forms.IntegerField(required=True)
    body = forms.CharField(required=True)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')

class SearchForm(forms.Form):
    query = forms.CharField()
