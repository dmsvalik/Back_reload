from django.contrib import admin

from .models import GalleryImages


@admin.register(GalleryImages)
class GalleryImagesAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "type_place", "price"]
