from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("",views.index),
    path("school/",views.school),
    path('shop/',views.shop),
    path('detail/<int:id>/',views.detail),
    path('product/<int:id>/',views.product),
    path('course/',views.course),
    path('afficient/',views.afficient),
    path("service/consult/",views.new_consult),
]
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

