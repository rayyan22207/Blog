from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from . import api_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("blog.urls")),
    path('profiles/', include("profiles.urls")),
    path('api/posts/<slug:slug>/like/', api_view.api_like_post, name='api_like_post'),
    path('api/posts/<slug:slug>/comment/', api_view.api_comment_post, name='api_comment_post'),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)