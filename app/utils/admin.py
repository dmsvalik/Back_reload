from django.contrib import admin

from .models import GalleryImages, GallerySlider


@admin.register(GallerySlider)
class GallerySliderAdmin(admin.ModelAdmin):
    """Админка слайдера."""

    list_display = ["id", "name"]


@admin.register(GalleryImages)
class GalleryImagesAdmin(admin.ModelAdmin):
    """Админка картинок слайдера."""

    list_display = ["id", "slider", "position", "name", "price"]
