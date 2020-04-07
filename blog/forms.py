from django import forms
from . import models

class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)

class CommentForm(forms.ModelForm):
    class Meta:
        model = models.Comment
        fields = ('name', 'email', 'body')


class SearchForm(forms.Form):
    query = forms.CharField()