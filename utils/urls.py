from django.urls import path

from utils.views import get_task_status, document_view, check_expired_auction_orders, GalleryImagesViewSet
from utils.initial_data_work import create_admin, create_users

urlpatterns = [

    path("create/admin/", create_admin, name="create_admin"),
    path("create/users/", create_users, name="create_users"),

    path("tasks/<task_id>/", get_task_status, name="get_task_status"),
    path("documents/<path:path>", document_view),

    path("check_expired_auction_orders/", check_expired_auction_orders),
    path("utils/gallery/<position>", GalleryImagesViewSet.as_view({"get": "list"})),
]
