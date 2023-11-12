from django.urls import path

from utils.views import get_task_status, document_view, check_expired_auction_orders, GalleryImagesViewSet
<<<<<<< HEAD
from utils.initial_data_work import create_admin, create_all_data
=======
from utils.prepare_db.initial_data_work import create_admin, create_all_data
>>>>>>> 236b3830cd8e1414fa5a97bf465922fd14b60104

urlpatterns = [

    path("create/admin/", create_admin, name="create_admin"),
    path("create/all_data/", create_all_data, name="create_all_data"),

    path("tasks/<task_id>/", get_task_status, name="get_task_status"),
    path("documents/<path:path>", document_view),

    path("check_expired_auction_orders/", check_expired_auction_orders),
    path("utils/gallery", GalleryImagesViewSet.as_view({"get": "list"})),
]
