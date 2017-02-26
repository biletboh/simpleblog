from .models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from form_utils import forms as betterforms
from django.db import models
from django_file_form.forms import FileFormMixin, UploadedFileField, MultipleUploadedFileField
from datetimewidget.widgets import DateWidget

class UserUpdateForm(FileFormMixin, betterforms.BetterForm):
    username = forms.CharField(required=False) 
    email = forms.EmailField(required=False)
    first_name = forms.CharField(required=False) 
    last_name = forms.CharField(required=False) 
    country = forms.CharField(required=False) 
    city = forms.CharField(required=False)
    birthday = forms.DateField(required=False, widget=DateWidget(usel10n=True, bootstrap_version=3, options = {
        'startView':4,
        }))
    avatar = UploadedFileField(label="Profile image", required = False)
    form_id = forms.CharField(widget = forms.HiddenInput(), required = False)
    upload_url = forms.CharField(widget = forms.HiddenInput(), required = False)
    delete_url = forms.CharField(widget = forms.HiddenInput(), required = False)

    class Meta:
        fieldsets = [('1', {'description': 'User Info', 'legend': 'main_info', 'fields': ['email', 'first_name', 'last_name'], }), 
                ('2', {'description': 'User Info', 'legend': 'user_profile', 'fields': ['country', 'city', 'birthday', 'avatar', 'form_id', 'upload_url', 'delete_url'], })]
