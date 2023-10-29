from django.db import models


def image_gallery_path(instance, filename):
    return "/".join(
        [
            "main_page_images",
            "gallery_images",
            filename,
        ]
    )


class GalleryImages(models.Model):
    IMAGE_PLACE = [
        ("1", 'первое маленькое изображение'),
        ("2", 'второе маленькое изображение'),
        ("3", 'большое снизу изображение'),
        ("4", 'большое справа изображение')
    ]

    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField("название для картинки", max_length=120, null=True, blank=True)
    price = models.CharField("цена за которую была выполнена", max_length=10, null=True, blank=True)
    type_place = models.CharField("место на макете", max_length=11, choices=IMAGE_PLACE, default="1")
    image = models.ImageField("Изображение", upload_to=image_gallery_path)
