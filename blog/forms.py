from .models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from form_utils import forms as betterforms
from django.db import models
from django_file_form.forms import FileFormMixin, UploadedFileField, MultipleUploadedFileField


class UserUpdateForm(FileFormMixin, betterforms.BetterForm):
    username = forms.CharField(required=False) 
    email = forms.EmailField(required=False)
    first_name = forms.CharField(required=False) 
    last_name = forms.CharField(required=False) 
    old_password = forms.CharField(required=False, label="Old Password", widget=forms.PasswordInput()) 
    password1 = forms.CharField(required=False, label="New Password", widget=forms.PasswordInput()) 
    password2 = forms.CharField(required=False, label="Confirm New Password", widget=forms.PasswordInput()) 

    country = forms.CharField(required=False) 
    city = forms.CharField(required=False)
#    organization = forms.CharField(required=False, label="Research oragnization (University)")
    avatar = UploadedFileField(label="Profile image", required = False)
    form_id = forms.CharField(widget = forms.HiddenInput(), required = False)
    upload_url = forms.CharField(widget = forms.HiddenInput(), required = False)
    delete_url = forms.CharField(widget = forms.HiddenInput(), required = False)

    class Meta:
        fieldsets = [('1', {'description': 'User Info', 'legend': 'main_info', 'fields': ['email', 'first_name', 'last_name', 'country', 'city', 'avatar', 'form_id', 'upload_url', 'delete_url'], })]
