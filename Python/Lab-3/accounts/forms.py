from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms

from accounts.models import UserProfile

attrs = {'class': 'form-control'}


class UserCreateForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs=attrs))
    password1 = forms.CharField(required=True, widget=forms.PasswordInput(attrs=attrs))
    username = forms.CharField(required=True, widget=forms.TextInput(attrs=attrs))
    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs=attrs))
    password2 = None

    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args, **kwargs)

        for filename in ['first_name', 'username', 'password1']:
            self.fields[filename].help_text = None


class AuthenticateForm(AuthenticationForm):
    username = forms.CharField(required=True, widget=forms.TextInput(attrs=attrs))
    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs=attrs))


class ImageForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image']
        exclude = ['is_official', 'description', 'header_image']


class HeaderImageForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['header_image']
        widgets = {
            'required': False,
            'header_image': forms.FileInput(attrs={
                'id': 'header-image-input',
                'type': "file",
                'name': "file",
                'accept': "image/gif, image/jpeg, image/png, image/webp"
            })
        }


class DescriptionForm(forms.ModelForm):
    class Meta:
        attrs = {
            'id': 'textarea',
            'autocomplete': 'on',
            'cols': '',
            'placeholder': 'Расскажите о себе',
            'rows': ''
        }

        model = UserProfile
        fields = ['description']
        widgets = {
            'label': 'Описание',
            'required': False,
            'description': forms.Textarea(attrs=attrs)
        }
