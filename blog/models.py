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
class BasePost(models.Model):
    body = HTMLField() 
    pub_date = models.DateTimeField(default=timezone.datetime.now)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    
    class Meta:
        ordering = ('-pub_date',)
# Post 
class Post(BasePost):
    name = models.CharField(max_length=200)
    image = ThumbnailerImageField(upload_to='photos/blog', blank=True) 
    
    def __str__(self):
        return self.name

# Comment
class Comment(BasePost):
    article = models.ForeignKey(Post, on_delete = models.CASCADE)

# Like Button
class Like(models.Model):
    user = models.ForeignKey(User)
    article = models.ForeignKey(Post, on_delete = models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.user_profile.save()
