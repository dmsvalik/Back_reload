"""
    Логика для работы с изображениями

"""

import os
from PIL import Image, ImageSequence

from config.settings import BASE_DIR, FILE_SETTINGS


class ImageWork(object):
    """Класс для работы с изображениями."""

    FILE_FORMAT = FILE_SETTINGS["IMAGE_FILE_FORMAT"]
    MAX_IMAGE_SIZE_IN_B = FILE_SETTINGS["MAX_IMAGE_SIZE_IN_B"]
    MAXIMUM_DIMENSIONS_OF_SIDES = FILE_SETTINGS["MAXIMUM_DIMENSIONS_OF_SIDES"]
    COEFFICIENT_OF_SIZE_CHANGING = FILE_SETTINGS[
        "IMAGE_COEFFICIENT_OF_SIZE_CHANGING"
    ]

    def __init__(self, temp_file, user_id, order_id=None):
        # there are may be without an order and user
        if order_id is None:
            order_id = "no_order"

        if user_id is None:
            user_id = "no_user"

        self.temp_file = temp_file
        self.relative_path = str(
            os.path.join(
                FILE_SETTINGS.get("PATH_ORDER_FILES"),
                str(user_id),
                str(order_id),
            )
        )
        self.dir_path = str(
            os.path.join(
                BASE_DIR,
                FILE_SETTINGS.get("PATH_SERVER_FILES"),
                self.relative_path,
            )
        )

        self.filename = temp_file.split("/")[-1]
        self.preview = self._prepare_and_save_preview()
        self.preview_path = self.preview.split(
            FILE_SETTINGS.get("PATH_SERVER_FILES") + "/"
        )[-1]
        self.upload_file_size = os.path.getsize(self._prepare_before_upload())
        self.preview_file_size = os.path.getsize(self.preview)

    def _prepare_and_save_preview(self):
        """Reducing the size of the image and saving it as a preview.
        The dimensions of the sides are no more than the established."""
        preview_path = os.path.join(self.dir_path, self.filename)

        img = Image.open(self.temp_file)
        img.thumbnail(self.MAXIMUM_DIMENSIONS_OF_SIDES)
        img.save(preview_path)
        return preview_path

    def _prepare_before_upload(self):
        """Preparing an image for uploading to Yandex Disk.
        The image file size is not more than 1 MB."""
        image_size = os.path.getsize(self.temp_file)
        img = Image.open(self.temp_file)
        while image_size > self.MAX_IMAGE_SIZE_IN_B:
            img = img.resize(
                (
                    int(img.size[0] * self.COEFFICIENT_OF_SIZE_CHANGING),
                    int(img.size[1] * self.COEFFICIENT_OF_SIZE_CHANGING),
                )
            )
            img.save(self.temp_file)
            image_size = os.path.getsize(self.temp_file)
        return self.temp_file


class GifWork(ImageWork):
    """Класс для работы с анимацией."""

    FILE_FORMAT = FILE_SETTINGS["ANIMATION_FILE_FORMAT"]
    COEFFICIENT_OF_SIZE_CHANGING = FILE_SETTINGS[
        "ANIMATION_COEFFICIENT_OF_SIZE_CHANGING"
    ]

    def _prepare_and_save_preview(self):
        """Reducing the size of the animation image and saving it as a preview.
        The dimensions of the sides are no more than the established."""
        # список для обработанных фреймов
        frames = []
        # откроем файл который создали ранее
        with Image.open(self.temp_file) as img:
            for frame in ImageSequence.Iterator(img):
                if frame.size[0] >= frame.size[1]:
                    reduction_ratio = (
                        self.MAXIMUM_DIMENSIONS_OF_SIDES[0] / frame.size[0]
                    )
                else:
                    reduction_ratio = (
                        self.MAXIMUM_DIMENSIONS_OF_SIDES[0] / frame.size[1]
                    )
                # и уменьшим согласно коэффициента
                size = (
                    int(frame.size[0] * reduction_ratio),
                    int(frame.size[1] * reduction_ratio),
                )
                frame = frame.resize(size)
                # добавляем обраборанный фрейм в список
                frames.append(frame)

        # сохраняем обработанное GIF-изображение
        preview_path = os.path.join(self.dir_path, self.filename)
        frames[0].save(
            preview_path,
            save_all=True,
            loop=0,
            append_images=frames[1:],
            optimize=False,
            duration=3,
        )
        return preview_path

    def _prepare_before_upload(self):
        """Preparing a gif for uploading to Yandex Disk.
        The gif file size is not more than 1 MB."""
        gif_size = os.path.getsize(self.temp_file)
        while gif_size > self.MAX_IMAGE_SIZE_IN_B:
            frames = []
            # откроем файл который создали ранее
            with Image.open(self.temp_file) as img:
                for frame in ImageSequence.Iterator(img):
                    # и уменьшим согласно коэффициента
                    size = (
                        int(frame.size[0] * self.COEFFICIENT_OF_SIZE_CHANGING),
                        int(frame.size[1] * self.COEFFICIENT_OF_SIZE_CHANGING),
                    )
                    frame = frame.resize(size)
                    # добавляем обраборанный фрейм в список
                    frames.append(frame)

            # сохраняем обработанное GIF-изображение
            frames[0].save(
                self.temp_file,
                save_all=True,
                loop=0,
                append_images=frames[1:],
                optimize=False,
                duration=3,
            )
            gif_size = os.path.getsize(self.temp_file)
        return self.temp_file
