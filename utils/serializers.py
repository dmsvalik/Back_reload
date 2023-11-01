from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import GalleryImages


class GalleryImagesSerializer(ModelSerializer):
    slider_number = serializers.CharField(source='slider.name')
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = GalleryImages
        fields = ["slider_number", "name", "image_url", "price", "position"]

    # change url without domain
    def get_image_url(self, galleryimages):
        image_url = galleryimages.image.url
        return image_url
