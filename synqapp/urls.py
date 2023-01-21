from django.urls import path
from . import views

urlpatterns = [
    path("synqapp/", views.index),
]
