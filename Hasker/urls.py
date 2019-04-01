from django.contrib import admin
from django.urls import path, include
from Hasker.settings import MEDIA_ROOT, MEDIA_URL, STATIC_URL, STATIC_ROOT
from django.conf.urls.static import static

try:
    from Hasker.local_settings import DEBUG
except ImportError as error:
    from Hasker.settings import DEBUG


urlpatterns = [
    path('', include('Hasker.profile.urls')),
    path('', include('Hasker.hasker.urls')),
    path('admin/', admin.site.urls),
]
if DEBUG:
    urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
    urlpatterns += static(STATIC_URL, document_root=STATIC_ROOT)
