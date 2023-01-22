from django.urls import path
from . import views

app_name = 'synqapp'


urlpatterns = [
    # path("", views.index),
    path("", views.welcome_page, name="welcome"),
    path("synqapp/album", views.album_page, name="album"),
    path("synqapp/upload", views.upload_page, name="upload"),
]
