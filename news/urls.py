from django.urls import path
from . import views

urlpatterns = [
    path("news/", views.news_list_view, name="news_list_view"),
    path("news/create/", views.news_create_view, name="news_create_view"),
    path("news/<str:news_id>/delete/", views.news_delete_view, name="news_delete_view"),
    path("news/<str:news_id>/", views.news_detail_view, name="news_detail_view"),
    path("news/<str:news_id>/update/", views.news_update_view, name="news_update_view"),
]
