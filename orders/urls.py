from django.urls import path

from .views import OrderImageViewSet, OrderOfferViewSet
from . import views

urlpatterns = [
    path("products/image", OrderImageViewSet.as_view({"get": "list", "post": "create"})),
    path("offers/", OrderOfferViewSet.as_view({"get": "list"})),
    path("offer/", OrderOfferViewSet.as_view({"post": "create"})),
    path("offer/<int:pk>/",OrderOfferViewSet.as_view({"get": "retrieve", "delete": "destroy", "put": "update"}),),

    path("order/image_upload_order/", views.upload_image_order, name='upload-image-order'),
    path("order/image_get_order/<int:file_id>", views.get_file_order, name="get-image-order"),
]
