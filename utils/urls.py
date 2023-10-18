from django.urls import path

from utils.views import get_task_status, document_view

urlpatterns = [
    path("tasks/<task_id>/", get_task_status, name="get_task_status"),
    path("documents/<path:path>", document_view),
]
