from django.urls import path

from app.file import views

urlpatterns = [
    path("upload/", views.CreateFileView.as_view(), name="upload_file")
]
