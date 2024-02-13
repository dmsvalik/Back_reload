from unittest.mock import ANY

import pytest
from app.file.storage.server import TmpServerFiles
from config.settings import FILE_SETTINGS


class TestTmpServerFiles:
    """Тест-кейс работы с файлами"""
    @pytest.mark.parametrize(
        "filename, result",
        [
            ("test.jpg", "jpg"),
            ("test.jpeg", "jpeg"),
            ("test.png", "png"),
            ("test.docx", "docx"),
            ("test.pdf", "pdf")
        ]
    )
    def test_get_file_format(self, filename, result):
        """Тест получения формата файла"""
        server_files = TmpServerFiles()
        assert server_files.get_file_format(filename) == result

    @pytest.mark.parametrize(
        "filename,file_format,length",
        [
            ("test.jpg",
             ".jpg",
             FILE_SETTINGS.get("NUMBER_OF_CHARACTERS_IN_FILENAME") + 4
             ),
            ("test.pdf",
             ".pdf",
             FILE_SETTINGS.get("NUMBER_OF_CHARACTERS_IN_FILENAME") + 4
             )
        ]
    )
    def test_get_unique_filename(self, filename, file_format, length):
        """Тест генерации рандомного имени файла"""
        server_files = TmpServerFiles()
        result = server_files.get_unique_filename(filename)
        assert result[-4:] == file_format
        assert len(result) == length
