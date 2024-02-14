import pytest

from app.file.exception import ThisNotFileError
from app.file.storage.server import ServerFiles
from config.settings import FILE_SETTINGS


class TestServerFiles:
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
        server_files = ServerFiles()
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
        server_files = ServerFiles()
        result = server_files.get_unique_filename(filename)
        assert result[-4:] == file_format
        assert len(result) == length

    @pytest.mark.parametrize(
        "lst,result", [
            (["test", "test", "test.jpg"], "test/test/test.jpg"),
            (["test1", "test1", "test.dox"], "test1/test1/test.dox")
        ]
    )
    def test_generate_path(self, lst, result):

        server_files = ServerFiles()
        res = server_files.generate_path(*lst)
        assert res == result

    @pytest.mark.parametrize(
        "path,result", [
            ("test/test/test.jpg", "test.jpg"),
            ("test1/test1/test.dox", "test.dox")
        ]
    )
    def test_get_filename_from_path(self, path, result):
        server_files = ServerFiles()
        res = server_files.get_filename_from_path(path)
        assert res == result

    def test_get_filename_from_path_invalid_path(self):
        server_files = ServerFiles()
        with pytest.raises(ThisNotFileError):
            server_files.get_filename_from_path("test1/test1/ggdgr")

    @pytest.mark.parametrize(
        "path,filename,result", [
            ("test/test/test.jpg", "test1.jpg", "test/test/test1.jpg"),
            ("test/test/test.dox", "test1.jpg", "test/test/test1.jpg"),
        ]
    )
    def test_replace_filename(self, path, filename, result):
        server_files = ServerFiles()
        res = server_files.replace_filename_from_path(path, filename)
        assert res == result

    @pytest.mark.parametrize(
        "path,filename", [
            ("test/test/testjpg", "test1.jpg"),
            ("test/test/test.dox", "test1jpg"),
        ]
    )
    def test_replace_filename_invalid(self, path, filename):

        server_files = ServerFiles()
        with pytest.raises(ThisNotFileError):
            server_files.replace_filename_from_path(path, filename)
