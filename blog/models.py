# basic imports 

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone

# import thumbnailer field to handle images

from easy_thumbnails.fields import ThumbnailerImageField

# import tinyMCE full text editor

from tinymce.models import HTMLField

# import signals to automatically create custom User Profile

from django.db.models.signals import post_save
from django.dispatch import receiver

# User Profile Model

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, unique=True, primary_key=True, on_delete=models.CASCADE, related_name='user_profile')
    avatar = ThumbnailerImageField(upload_to='profile_images', blank=True)
    birthday = models.DateField(null=True, blank=True)
    country = models.CharField(max_length = 128, blank=True)
    city = models.CharField(max_length = 128, blank=True)

    def __unicode__(self):
        return self.user.username


# Post Model

class Post(models.Model):
    name = models.CharField(max_length=200)
    body = HTMLField() 
    pub_date = models.DateTimeField(default=timezone.datetime.now)
    image = ThumbnailerImageField(upload_to='photos/blog', blank=True) 
    
    class Meta:
        ordering = ('-pub_date',)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.user_profile.save()
