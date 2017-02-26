from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static


urlpatterns = [
    # basic urls
    url(r'^', include('blog.urls')),
    url(r'^admin/', admin.site.urls),
    
    # email verification urls
    url(r'^accounts/', include('allauth.urls')),

    # uploads
    url(r'^upload/', include('django_file_form.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
