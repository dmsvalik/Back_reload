from django.urls import path

from app.file import views

urlpatterns = [path("file/", views.FileView.as_view(), name="upload_file")]
