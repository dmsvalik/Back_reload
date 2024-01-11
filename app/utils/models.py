from django.db import models


def image_gallery_path(instance, filename):
    """Создание пути сохранения изображения для слайдера."""
    return "/".join(
        [
            "main_page_images",
            "gallery_images",
            filename,
        ]
    )


class GallerySlider(models.Model):
    """Модель слайдера."""

    SLIDER_NAME = [
        ("1", "первый слайдер"),
        ("2", "второй слайдер"),
        ("3", "третий слайдер"),
    ]

    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(
        "название слайдера по позиции в макете",
        max_length=11,
        choices=SLIDER_NAME,
        unique=True,
    )

    class Meta:
        verbose_name = "Слайдер галереи"
        verbose_name_plural = "Слайдер галереи"

    def __str__(self):
        return self.name


class GalleryImages(models.Model):
    """Модель изображения для слайдера с указанием позиции."""

    IMAGE_PLACE = [
        ("1", "первое маленькое изображение"),
        ("2", "второе маленькое изображение"),
        ("3", "большое снизу изображение"),
        ("4", "большое справа изображение"),
    ]

    id = models.AutoField(primary_key=True, unique=True)
    slider = models.ForeignKey(
        GallerySlider, on_delete=models.CASCADE, null=True
    )
    name = models.CharField(
        "название для картинки", max_length=120, null=True, blank=True
    )
    price = models.CharField(
        "цена за которую был выполнен заказ",
        max_length=10,
        null=True,
        blank=True,
    )
    position = models.CharField(
        "место на макете - слева направо",
        max_length=11,
        choices=IMAGE_PLACE,
        default="1",
    )
    image = models.ImageField("Изображение", upload_to=image_gallery_path)

    class Meta:
        verbose_name = "Изображения к слайдерами"
        verbose_name_plural = "Изображения к слайдерами"
