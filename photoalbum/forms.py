from django import forms
from photoalbum.models import UserModel, Comment


class LoginForm(forms.Form):
    username = forms.EmailField(label='Nazwa użytkownika')
    password = forms.CharField(label='Hasło', widget=forms.PasswordInput)


class AddUserForm(forms.Form):
    username = forms.EmailField(label='Nazwa użytkownika')
    password = forms.CharField(label='Hasło', widget=forms.PasswordInput)


class UploadPhotoForm(forms.Form):
    file = forms.ImageField(label='Dodaj zdjęcie')


class EditUserForm(forms.ModelForm):
    password = forms.CharField(max_length=128, widget=forms.PasswordInput, label='Password')
    class Meta:
        model = UserModel
        fields = ['username', 'first_name', 'last_name', 'email']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']