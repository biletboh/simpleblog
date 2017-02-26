from django.conf.urls import url

from . import views

app_name = 'blog'

urlpatterns = [
        url(r'^$', views.WelcomePage.as_view(), name = 'welcome'),
        url(r'accounts/profile/(?P<pk>[0-9]+)/$', 
            views.UserProfile.as_view(), name='profile'),
]
