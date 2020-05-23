from django import forms
from . import models

attrs = {
    'id': 'textarea',
    'autocomplete': 'on',
    'cols': '',
}


class SearchForm(forms.ModelForm):
    attrs['autofocus'] = ''
    attrs['class'] = 'form-control'
    content = forms.CharField(label='', required=True, max_length=160, widget=forms.TextInput(attrs=attrs))

    class Meta:
        model = models.Tweet
        fields = ['content']


class CreateTwit(forms.ModelForm):
    attrs['placeholder'] = 'Что происходит?'
    attrs['rows'] = ''
    content = forms.CharField(widget=forms.Textarea(attrs=attrs), label='', required=True, max_length=235)

    class Meta:
        model = models.Tweet
        fields = ['content', 'image']


class CommentForm(forms.ModelForm):
    attrs['placeholder'] = 'Что скажешь?'
    attrs['rows'] = ''
    content = forms.CharField(widget=forms.Textarea(attrs=attrs), label='', required=True, max_length=235)

    class Meta:
        model = models.Comment
        fields = ['content']
