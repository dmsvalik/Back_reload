from django.urls import path

from app.utils.views import (
    get_task_status,
    document_view,
    check_expired_auction_orders,
    GalleryImagesViewSet,
    AllDeleteAPIView,
    get_order_pdf,
)
from app.utils.prepare_db.initial_data_work import (
    create_admin,
    create_all_data,
)


urlpatterns = [
    path("create/admin/", create_admin, name="create_admin"),
    path("create/all_data/", create_all_data, name="create_all_data"),
    path("tasks/<task_id>/", get_task_status, name="get_task_status"),
    path("documents/<path:path>", document_view, name="document-view"),
    path("check_expired_auction_orders/", check_expired_auction_orders),
    path("utils/gallery/", GalleryImagesViewSet.as_view({"get": "list"})),
    path("order/<int:pk>/get_order_pdf/", get_order_pdf, name="get-order-pdf"),
    path(
        "delete_all/", AllDeleteAPIView.as_view({"delete": "delete_all_view"})
    ),
]
