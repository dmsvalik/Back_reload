from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from config.settings import DOMAIN

from .models import GalleryImages


class GalleryImagesSerializer(ModelSerializer):
    # Поменяны местами вывод slider_number и position. Ошибка на стороне фронта
    position = serializers.CharField(source="slider.name")
    image_url = serializers.SerializerMethodField()
    slider_number = serializers.CharField(source="position")

    class Meta:
        model = GalleryImages
        fields = [
            "id",
            "slider_number",
            "name",
            "image_url",
            "price",
            "position",
        ]

    # change url without domain
    def get_image_url(self, galleryimages):
        icon_url = galleryimages.image.url
        return f"https://{DOMAIN}{icon_url}"
