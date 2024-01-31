from django.urls import path, include

from . import views


urlpatterns = [
    path(
        "orders/<int:pk>/",
        include(
            [
                path(
                    "answers/",
                    views.create_answers_to_order,
                    name="post-order-answers",
                ),
                path(
                    "finish/",
                    views.OrderStateActivateView.as_view(),
                    name="order-activate",
                ),
                path("files/", views.attach_file, name="file attach"),
                path(
                    "offers/",
                    views.OrderOfferView.as_view(),
                ),
            ]
        ),
    ),
    path(
        "order/last/",
        views.get_answers_to_last_order,
        name="get-last-order-answers",
    ),
    path(
        "offers/<int:pk>/",
        views.OfferViewSet.as_view(
            {"get": "retrieve", "delete": "destroy", "put": "update"}
        ),
    ),
    path("order/create/", views.create_order, name="order-create"),
    path(
        "order/client/all_orders/",
        views.AllOrdersClientViewSet.as_view({"get": "list"}),
    ),
    path(
        "order/client/archive/",
        views.ArchiveOrdersClientViewSet.as_view({"get": "list"}),
    ),
    path(
        "order/file_order/", views.delete_file_order, name="delete-file-order"
    ),
    path(
        "order/download/<str:file_id>/",
        views.get_download_file_link,
        name="get-download-link",
    ),
    path("order/clone/", views.CloneOrderView.as_view(), name="order_clone"),
]
