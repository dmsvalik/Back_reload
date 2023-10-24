import os

from config.settings import BASE_DIR
from main_page.models import UserAccount


class FileWork(object):
    """Class for working with uploaded files."""

    def __init__(self, temp_file, user_id, order_id=None):
        if order_id is None:
            order_id = 'no_order'

        self.temp_file = temp_file
        self.user = UserAccount.objects.get(id=user_id)
        self.order = order_id
        self.dir_path = os.path.join(BASE_DIR, "media_type")
        self.filename = temp_file.split('/')[-1]
        self.upload_file_size = self._upload_file_size()
        self.preview_file_size = self._preview_file_size()

    def preview_path(self):
        """Preparing preview path"""
        return os.path.join(self.dir_path, f"{self.temp_file.split('.')[-1]}_thumbnails.jpg")

    def _upload_file_size(self):
        """Calculating the file size."""
        return os.path.getsize(self.temp_file)

    def _preview_file_size(self):
        """Calculating the preview file size"""
        return os.path.getsize(self.preview_path())
