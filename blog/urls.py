from django.conf.urls import url

from . import views

app_name = 'blog'

urlpatterns = [
        url(r'^$', views.WelcomePage.as_view(), name = 'welcome'),

        # user management
        url(r'accounts/profile/(?P<pk>[0-9]+)/$', 
            views.UserProfile.as_view(), name='profile'),
        url(r'user/update/(?P<pk>[0-9]+)/$', views.UserUpdate.as_view(), name = 'update-profile'),
        url(r'user/delete/(?P<pk>[0-9]+)/$', views.UserDelete.as_view(), name = 'user-delete'),

        # post management 
        url(r'post/add/$', views.CreatePost.as_view(), name = 'create-post'),
        url(r'^blog/post/delete/(?P<pk>\d+)/$', views.DeletePost.as_view(), name='delete-post'),
        url(r'^blog/post/edit/(?P<pk>\d+)/$', views.EditPost.as_view(), name='edit-post'),

        # blog
        url(r'blog/$', views.Blog.as_view(), name = 'blog'),
        url(r'blog/post/(?P<pk>[0-9]+)/$', views.PostPage.as_view(), name = 'post-page'),
]
