from django.urls import path

from . import views
from .views import (
    AllOrdersClientViewSet,
    ArchiveOrdersClientViewSet,
    OrderOfferViewSet,
)


urlpatterns = [
    path("order/<int:pk>/offers/", OrderOfferViewSet.as_view({"get": "list"})),
    path(
        "order/<int:pk>/offer/", OrderOfferViewSet.as_view({"post": "create"})
    ),
    path(
        "order/<int:pk>/answers/",
        views.create_answers_to_order,
        name="post-order-answers",
    ),
    path(
        "order/<int:pk>/", views.get_answers_to_order, name="get-order-answers"
    ),
    path(
        "offer/<int:pk>/",
        OrderOfferViewSet.as_view(
            {"get": "retrieve", "delete": "destroy", "put": "update"}
        ),
    ),
    path("order/create/", views.create_order, name="order-create"),
    path(
        "order/client/all_orders/",
        AllOrdersClientViewSet.as_view({"get": "list"}),
    ),
    path(
        "order/client/archive/",
        ArchiveOrdersClientViewSet.as_view({"get": "list"}),
    ),
    path(
        "order/file_order/", views.delete_file_order, name="delete-file-order"
    ),
    path("order/<int:pk>/files/", views.attach_file, name="file attach"),
    path(
        "download/<str:file_id>/",
        views.get_download_file_link,
        name="get-download-link",
    ),
    path(
        "order/<int:pk>/finish/",
        views.OrderStateActivateView.as_view(),
        name="order-activate",
    ),
    path("order/clone/", views.CloneOrderView.as_view(), name="order_clone"),
]
