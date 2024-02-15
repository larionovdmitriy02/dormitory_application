from django.urls import path
from . import views

urlpatterns = [
    path("student/all/", views.student_list_view, name="student_list_view"),
    path("login/", views.student_login_view, name="student_login_view"),
    path("logout/", views.student_logout_view, name="student_logout_view"),
    path("student/create/", views.student_create_view, name="student_create_view"),
    path("student/rating", views.student_rating_view, name="student_rating_view"),
    path(
        "student/file/<str:file_id>/download",
        views.student_download_document_view,
        name="student_download_document_view",
    ),
    path(
        "student/<str:student_id>/file/<str:file_id>/delete/",
        views.student_document_delete_view,
        name="student_document_delete_view",
    ),
    path(
        "student/<str:student_id>/works/all",
        views.student_work_list_view,
        name="student_work_list_view",
    ),
    path(
        "student/<str:student_id>/file/upload/",
        views.student_upload_document_view,
        name="student_upload_document_view",
    ),
    path(
        "student/<str:student_id>/",
        views.student_detail_view,
        name="student_detail_view",
    ),
    path(
        "student/<str:student_id>/update",
        views.student_update_view,
        name="student_update_view",
    ),
    path(
        "student/<str:student_id>/delete",
        views.student_delete_view,
        name="student_delete_view",
    ),
]
