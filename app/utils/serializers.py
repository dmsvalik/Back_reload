from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import GalleryImages


class GalleryImagesSerializer(ModelSerializer):
    slider_number = serializers.CharField(source='slider.name')
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = GalleryImages
        fields = ["id", "slider_number", "name", "image_url", "price", "position"]

    # change url without domain
    def get_image_url(self, galleryimages):
        request = self.context.get('request')
        icon_url = galleryimages.image.url
        return request.build_absolute_uri(icon_url)
