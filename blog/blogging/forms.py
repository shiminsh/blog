from django import forms
from django.contrib import auth
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Blog


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget = forms.TextInput(
                             attrs={'placeholder': 'Username', 'class':'form-control'})
        self.fields['username'].label = "Username"
        self.fields['email'].widget = forms.TextInput(
                             attrs={'placeholder': 'Email', 'class':'form-control'})
        self.fields['email'].label = "Email"
        self.fields['password1'].widget = forms.PasswordInput(
                             attrs={'placeholder': 'Password', 'class': 'form-control'})
        self.fields['password1'].label = "Password"
        self.fields['password2'].widget = forms.PasswordInput(
                             attrs={'placeholder': 'Re-enter your password', 'class': 'form-control'})
        self.fields['password2'].label = "Confirm Password"

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email=self.cleaned_data['email']

        if commit:
           user.save()

        return user

    def clean_email(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        email = self.cleaned_data["email"]
        try:
            User._default_manager.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError('An account with this email already exists.')
        

class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget = forms.TextInput(
                             attrs={'placeholder': 'Username', 'class':'form-control'})
        self.fields['username'].label = "Username"
        self.fields['password'].widget = forms.PasswordInput(
                             attrs={'placeholder': 'Password', 'class': 'form-control'})
        self.fields['password'].label = "Password"


class BlogForm(forms.ModelForm):

    class Meta:
        model = Blog
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        super(BlogForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget = forms.TextInput(
                             attrs={'placeholder': 'Title', 'class':'form-control'})
        self.fields['title'].label = "Title"
        self.fields['description'].widget = forms.Textarea(
                             attrs={'class': 'form-control', 'rows': 30, 'cols': 90 })
        self.fields['description'].label = "Enter Description"


