from django.urls import path

from . import views
from .views import AllOrdersClientViewSet, ArchiveOrdersClientViewSet, OrderOfferViewSet


urlpatterns = [
    path("order/<int:pk>/offers/", OrderOfferViewSet.as_view({"get": "list"})),
    path("order/<int:pk>/offer/", OrderOfferViewSet.as_view({"post": "create"})),
    path("order/<int:pk>/answers/", views.create_answers_to_oder, name="post-order-answers",),
    path("order/<int:pk>/", views.get_answers_to_oder, name="get-order-answers"),
    path("offer/<int:pk>/", OrderOfferViewSet.as_view({"get": "retrieve", "delete": "destroy", "put": "update"}),),

    path("order/create/", views.create_order, name='order-create'),
    path("order/image_upload_order/", views.upload_image_order, name='upload-image-order'),
    path("order/image_get_order/<int:file_id>", views.get_file_order, name="get-image-order"),
    path("order/client/all_orders", AllOrdersClientViewSet.as_view({"get": "list"})),
    path("order/client/archive", ArchiveOrdersClientViewSet.as_view({"get": "list"})),
    path("order/delete_file_order/", views.delete_file_order, name='delete-file-order'),

]
