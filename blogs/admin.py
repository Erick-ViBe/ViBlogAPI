from django.contrib import admin

from blogs.models import Tag, Blog


admin.site.register(Tag)
admin.site.register(Blog)
