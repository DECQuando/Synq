from django.urls import path
from . import views

app_name = 'synqapp'


urlpatterns = [
    path("", views.welcome_page, name="welcome"),
    path("synqapp/post/", views.ImagePost.as_view(), name="image_post"),
    path("synqapp/list/", views.ImageList.as_view(), name="image_list"),
    path("synqapp/detail/<int:pk>/", views.ImageDetail.as_view(), name='image_detail'),
    # グルーピングなしのアルバム表示
    path('synqapp/list-no-grouping/', views.ImageListNoGrouping.as_view(), name='image_list_no_grouping'),
]
