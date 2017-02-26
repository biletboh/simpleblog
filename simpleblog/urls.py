from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin


urlpatterns = [
    # basic urls
    url(r'^', include('blog.urls')),
    url(r'^admin/', admin.site.urls),
    
    # email verification urls
    url(r'^accounts/', include('allauth.urls')),
]
