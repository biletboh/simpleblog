from django import forms
from form_utils import forms as betterforms

from django.db import models
from .models import UserProfile, Like

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from django.forms import ModelForm

from django_file_form.forms import FileFormMixin, UploadedFileField, MultipleUploadedFileField

from django.utils import timezone
from django.forms.widgets import HiddenInput
from datetimewidget.widgets import DateWidget, DateTimeWidget
from tinymce.widgets import TinyMCE

class UserUpdateForm(FileFormMixin, betterforms.BetterForm):
    username = forms.CharField(required=False) 
    email = forms.EmailField(required=False)
    first_name = forms.CharField(required=False) 
    last_name = forms.CharField(required=False) 
    country = forms.CharField(required=False) 
    city = forms.CharField(required=False)
    birthday = forms.DateField(required=False, initial=timezone.now, widget=DateWidget(usel10n=True, bootstrap_version=3, options = {
        'startView':4,
        }))
    avatar = UploadedFileField(label="Profile image", required = False)
    form_id = forms.CharField(widget = forms.HiddenInput(), required = False)
    upload_url = forms.CharField(widget = forms.HiddenInput(), required = False)
    delete_url = forms.CharField(widget = forms.HiddenInput(), required = False)

    class Meta:
        fieldsets = [('1', {'description': 'User Info', 'legend': 'main_info', 'fields': ['email', 'first_name', 'last_name'], }), 
                ('2', {'description': 'User Info', 'legend': 'user_profile', 'fields': ['country', 'city', 'birthday', 'avatar', 'form_id', 'upload_url', 'delete_url'], })]


class PostForm(FileFormMixin, betterforms.BetterForm):
    name = forms.CharField(label="name", max_length=200)
    body = forms.CharField(label="body", widget=TinyMCE(attrs={'cols': 80, 'rows': 30}), required=False)
    pub_date = forms.DateTimeField(label="publication date", widget=DateTimeWidget(usel10n=True, bootstrap_version=3), initial=timezone.now)
    image = UploadedFileField(label="image", required = False)
    form_id = forms.CharField(widget = forms.HiddenInput(), required = False)
    upload_url = forms.CharField(widget = forms.HiddenInput(), required = False)
    delete_url = forms.CharField(widget = forms.HiddenInput(), required = False)
    object_id = forms.CharField(widget = forms.HiddenInput(), required = False)

    class Meta:
        fieldsets = [
                ('main', {'fields': ['name', 'language', 'pub_date'], 
                    'legend': 'main', }),
                ('text-area', {'fields': ['body'], 'legend': 'text-area'}),
                ('images', {'fields': ['image'] + ['form_id', 'upload_url', 'delete_url'], 'legend': 'images'}),
                     ]
class CommentForm(FileFormMixin, betterforms.BetterForm):
    body = forms.CharField(label="body", widget=TinyMCE(attrs={'cols': 80, 'rows': 10}), required=False)
    class Meta:
        fieldsets = [('comment', {'fields': ['body'], 'legend': 'text-area'}),]

class LikeForm(betterforms.BetterForm):
    form_id = forms.CharField(widget = forms.HiddenInput(), required = False)
    class Meta:
        fieldsets = [
                ('likes', {'fields': ['form_id', ], 'legend': 'likes'}),
                ]

class BlogFilterForm(betterforms.BetterForm):
    name = forms.CharField(label="name", max_length=200, required = False)
    country = forms.CharField(label="country", max_length=200, required = False)
    city = forms.CharField(label="city", max_length=200, required = False)
    class Meta:
        fieldsets = [
                ('likes', {'fields': ['name','country', 'city' ], 'legend': 'likes'}),
                ]

