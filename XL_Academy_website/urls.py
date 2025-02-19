from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler404, handler500
from main.views import error_view
from  management.views import google_auth,google_callback

urlpatterns = [
    path('admin/', admin.site.urls),
    path('management/', include('management.urls')),
    path("", include('main.urls')),
    path('auth/', include('social_django.urls', namespace='social')),
    path("auth/", google_auth, name="google_auth"),
    path("auth/callback/", google_callback, name="google_callback"),

]
handler404 = error_view
handler403 = error_view
handler500 = error_view
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)