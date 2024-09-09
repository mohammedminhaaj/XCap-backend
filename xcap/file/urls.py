from django.urls import path
from . import views

urlpatterns = [
    path("get-user-files/", views.get_user_files, name="get_user_files"),
    path("upload-file/", views.upload_file, name="upload_file"),
]
