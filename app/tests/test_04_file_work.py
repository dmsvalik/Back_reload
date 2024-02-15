import os

import pytest

from app.file import exception as ex
from app.file.methods.file_work import FileWorkBase, TmpFileWork, \
    OfferFileWork
from app.file.storage.server import ServerFiles, ServerFileBase
from config.settings import FILE_SETTINGS, BASE_DIR


class TestFileWorkBase:

    def test_init(self):
        """Тест инициализации"""
        test = FileWorkBase()
        assert test.relative_path is None

    @pytest.mark.parametrize(
        "lst,result", [
            (["test", "test", "test.jpg"], "test/test/test.jpg"),
            (["test1", "test1", "test.dox"], "test1/test1/test.dox"),
            ([1, 5, 0.4], "1/5/0.4")
        ]
    )
    def test_get_path(self, lst, result):
        """Тест генерации пути из списка"""
        test = FileWorkBase()
        assert test.get_path(*lst) == result

    @pytest.mark.parametrize(
        "lst", [
            (["test"]),
            ([]),
        ]
    )
    def test_get_path_invalid(self, lst):
        """Тест вызова ошибки при неверной передаче данных"""
        test = FileWorkBase()
        with pytest.raises(ex.FewElementsError):
            test.get_path(*lst)


class TestTmpFileWork:
    def test_init(self):
        """Тест инициализации"""
        test = TmpFileWork()
        assert test.relative_path == FILE_SETTINGS.get("PATH_TMP_FILES")


class TestOfferFileWork:

    @pytest.mark.parametrize(
        "user_id,offer_id,result", [
            (5, 3, f"{FILE_SETTINGS.get('PATH_OFFER_FILES')}/5/3"),
            (10, 10, f"{FILE_SETTINGS.get('PATH_OFFER_FILES')}/10/10")
        ]
    )
    def test_init(self, user_id, offer_id, result):
        """Тест инициализации"""
        test = OfferFileWork(user_id, offer_id)
        assert test.relative_path == result
