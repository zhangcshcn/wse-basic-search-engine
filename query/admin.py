from django.contrib import admin

# Register your models here.
from .models import Docs, IndexedUrl

admin.site.register(Docs)
admin.site.register(IndexedUrl)