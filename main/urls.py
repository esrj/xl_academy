from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("",views.index),
    path("consult/",views.consult), # 最早的後來被要求改成 about
    path('shop/',views.shop),
    path('detail/<int:id>/',views.detail),
    path('product/<int:id>/',views.product),
    path('course/',views.course),
    path('afficient/',views.afficient),
    path("service/consult/",views.new_consult), # 結果又叫我在寫一次 ..
]
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

