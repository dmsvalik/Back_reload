from django.urls import path

from utils.views import get_task_status

urlpatterns = [
    path("tasks/<task_id>/", get_task_status, name="get_task_status"),
]
