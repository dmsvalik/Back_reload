from django.urls import path

from utils.views import get_task_status, document_view, check_expired_auction_orders

urlpatterns = [
    path("tasks/<task_id>/", get_task_status, name="get_task_status"),
    path("documents/<path:path>", document_view),

    path("check_expired_auction_orders/", check_expired_auction_orders),
]
