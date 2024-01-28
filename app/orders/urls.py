from django.urls import path, include

from . import views


urlpatterns = [
    path(
        "orders/<int:pk>/",
        include(
            [
                path(
                    "",
                    views.get_answers_to_order,
                    name="get-order-answers",
                ),
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
    path("create/", views.create_order, name="order-create"),
    path(
        "client/all_orders/",
        views.AllOrdersClientViewSet.as_view({"get": "list"}),
    ),
    path(
        "client/archive/",
        views.ArchiveOrdersClientViewSet.as_view({"get": "list"}),
    ),
    path("file_order/", views.delete_file_order, name="delete-file-order"),
    path(
        "download/<str:file_id>/",
        views.get_download_file_link,
        name="get-download-link",
    ),
]
