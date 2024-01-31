from django.contrib import admin
from .models import Contact,Profile,Collage,TestQuestion

admin.site.register(Profile)
admin.site.register(Contact)
admin.site.register(Collage)
admin.site.register(TestQuestion)

