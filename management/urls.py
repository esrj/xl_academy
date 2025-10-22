from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("contact/",views.contact),
    path("logout/",views.logout),
    path("",views.login),
    path('upload/',views.upload),
    path('collage/',views.collage),
    path('single/<int:id>/',views.single),
]
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

