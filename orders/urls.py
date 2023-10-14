from django.urls import path

from . import views
from .views import OrderModelMinifieldViewSet, OrderOfferViewSet


urlpatterns = [
    path("order/<int:pk>/offers/", OrderOfferViewSet.as_view({"get": "list"})),
    path("order/<int:pk>/offer/", OrderOfferViewSet.as_view({"post": "create"})),
    path("offer/<int:pk>/", OrderOfferViewSet.as_view({"get": "retrieve", "delete": "destroy", "put": "update"}),),

    path("order/image_upload_order/", views.upload_image_order, name='upload-image-order'),
    path("order/image_get_order/<int:file_id>", views.get_file_order, name="get-image-order"),
    path("order/client/all_orders", OrderModelMinifieldViewSet.as_view({"get": "list"})),
]
