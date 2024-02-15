from django.urls import path
from . import views

urlpatterns = [
    path(
        "dormitory/create/", views.dormitory_create_view, name="dormitory_create_view"
    ),
    path("dormitories/", views.dormitory_list_view, name="dormitory_list_view"),
    path(
        "dormitory/<str:dormitory_id>/delete/",
        views.dormitory_delete_view,
        name="dormitory_delete_view",
    ),
    path(
        "dormitory/<str:dormitory_id>/",
        views.dormitory_detail_view,
        name="dormitory_detail_view",
    ),
    path(
        "dormitory/<str:dormitory_id>/update/",
        views.dormitory_update_view,
        name="dormitory_update_view",
    ),
]
