from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import GalleryImages
from django.core.files import File

import base64


class GalleryImagesSerializer(ModelSerializer):
    base64_image = serializers.SerializerMethodField()

    class Meta:
        model = GalleryImages
        fields = ["id", "name", "price", "type_place", "base64_image"]

    def get_base64_image(self, obj):
        f = open(obj.image.path, 'rb')
        image = File(f)
        data = base64.b64encode(image.read())
        f.close()
        return data
