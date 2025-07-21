from django.contrib import admin
from .models import Song


@admin.register(Song)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'album', 'artist', 'slug', 'image', 'created']
    list_filter = ['created']
