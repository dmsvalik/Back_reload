import pytest
from app.file.storage.cloud import CloudBase


class TestCloudBase:

    @pytest.mark.parametrize(
        "path_item", [
            ["orders", "user_test", "order_test"],
            ["offers", "user_test", "offer_test"]
        ],
    )
    def test_get_path(self, path_item):

        file = CloudBase()

        path = file.get_path(*path_item)
        assert path == "/".join(path_item)
