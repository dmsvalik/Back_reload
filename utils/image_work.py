""" логика для работы с изображениями """
import os
import string
from pathlib import Path
import random
from PIL import Image, ImageSequence

from config.settings import BASE_DIR
from main_page.models import UserAccount
from orders.models import OrderModel


class ImageWork(object):
    FILE_FORMAT = 'jpg'
    MAX_IMAGE_SIZE_IN_B = 1024 * 1024
    MAXIMUM_DIMENSIONS_OF_SIDES = (300, 300)
    COEFFICIENT_OF_SIZE_CHANGING = 0.9
    NUMBER_OF_CHARACTERS_IN_FILENAME = 7

    def __init__(self, temp_file, user_id, order_id):
        self.temp_file = temp_file
        self.user = UserAccount.objects.get(id=user_id)
        self.order = OrderModel.objects.get(id=order_id)
        self.dir_path = os.path.join(BASE_DIR, "files", str(self.user.id), str(self.order.id))
        self.filename = self._generate_new_filename(self.dir_path, self.FILE_FORMAT)
        self.preview_path = self._prepare_and_save_preview()
        self.upload_file_size = os.path.getsize(self._prepare_before_upload())
        self.preview_file_size = os.path.getsize(self.preview_path)

    def _generate_new_filename(self, dir_path, file_format):
        """File Name generation."""
        existed_names = self._prepare_catalog_file_names(dir_path)
        generated_file_name = ''.join(random.choices(
            string.ascii_letters + string.digits,
            k=self.NUMBER_OF_CHARACTERS_IN_FILENAME
        ))
        while generated_file_name in existed_names:
            generated_file_name = ''.join(random.choices(
                string.ascii_letters + string.digits,
                k=self.NUMBER_OF_CHARACTERS_IN_FILENAME
            ))
        return f'{generated_file_name}.{file_format}'

    def _prepare_catalog_file_names(self, dir_path):
        """Parsing a list of all file names in the user's order directory."""
        res = []
        if Path(dir_path).is_dir():
            for path in os.listdir(dir_path):
                # check if current path is a file
                if os.path.isfile(os.path.join(dir_path, path)):
                    filename = path.split('.')[0]
                    res.append(filename)
        else:
            os.makedirs(dir_path)
        return res

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
                (int(img.size[0] * self.COEFFICIENT_OF_SIZE_CHANGING),
                 int(img.size[1] * self.COEFFICIENT_OF_SIZE_CHANGING))
            )
            img.save(self.temp_file)
            image_size = os.path.getsize(self.temp_file)
        return self.temp_file


class GifWork(ImageWork):
    FILE_FORMAT = 'gif'
    COEFFICIENT_OF_SIZE_CHANGING = 0.7

    def _prepare_and_save_preview(self):
        """Reducing the size of the animation image and saving it as a preview.
        The dimensions of the sides are no more than the established."""
        # список для обработанных фреймов
        frames = []
        # откроем файл который создали ранее
        with Image.open(self.temp_file) as img:
            for frame in ImageSequence.Iterator(img):
                if frame.size[0] >= frame.size[1]:
                    reduction_ratio = self.MAXIMUM_DIMENSIONS_OF_SIDES[0] / frame.size[0]
                else:
                    reduction_ratio = self.MAXIMUM_DIMENSIONS_OF_SIDES[0] / frame.size[1]
                # и уменьшим согласно коэффициента
                size = (int(frame.size[0] * reduction_ratio), int(frame.size[1] * reduction_ratio))
                frame = frame.resize(size)
                # добавляем обраборанный фрейм в список
                frames.append(frame)

        # сохраняем обработанное GIF-изображение
        preview_path = os.path.join(self.dir_path, self.filename)
        frames[0].save(preview_path, save_all=True, loop=0,
                       append_images=frames[1:], optimize=False, duration=3)
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
                    size = (int(frame.size[0] * self.COEFFICIENT_OF_SIZE_CHANGING),
                            int(frame.size[1] * self.COEFFICIENT_OF_SIZE_CHANGING))
                    frame = frame.resize(size)
                    # добавляем обраборанный фрейм в список
                    frames.append(frame)

            # сохраняем обработанное GIF-изображение
            frames[0].save(self.temp_file, save_all=True, loop=0,
                           append_images=frames[1:], optimize=False, duration=3)
            gif_size = os.path.getsize(self.temp_file)
        return self.temp_file
