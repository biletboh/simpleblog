from django.conf.urls import url

from . import views

app_name = 'blog'

urlpatterns = [
        url(r'^$', views.WelcomePage.as_view(), name = 'welcome'),
        url(r'accounts/profile/(?P<pk>[0-9]+)/$', 
            views.UserProfile.as_view(), name='profile'),
        url(r'user/update/(?P<pk>[0-9]+)/$', views.UserUpdate.as_view(), name = 'update-profile'),
        url(r'user/delete/(?P<pk>[0-9]+)/$', views.UserDelete.as_view(), name = 'user-delete'),
]
