from django.urls import path
from . import views

urlpatterns = [
    path(
        "work/administrative/create/",
        views.work_administrative_create_view,
        name="work_administrative_create_view",
    ),
    path(
        "work/<str:work_id>/students/all/end/",
        views.work_student_all_end,
        name="work_student_all_end",
    ),
    path(
        "work/activity/create/",
        views.work_activity_create_view,
        name="work_activity_create_view",
    ),
    path("work/all/", views.work_list_view, name="work_list_view"),
    path(
        "work/<str:work_id>/student/<str:student_id>/ready/",
        views.work_student_ready_view,
        name="work_student_ready_view",
    ),
    path("work/<str:work_id>/finish/", views.work_finish_view, name="work_finish_view"),
    path(
        "work/<str:work_id>/student/all/",
        views.work_student_list_view,
        name="work_student_list_view",
    ),
    path(
        "work/<str:work_id>/student/<str:student_id>/add/",
        views.add_student_to_work_view,
        name="add_student_to_work_view",
    ),
    path("work/<str:work_id>/", views.work_detail_view, name="work_detail_view"),
    path(
        "work/<str:work_id>/take/",
        views.work_take_part_view,
        name="work_take_part_view",
    ),
    path(
        "work/<str:work_id>/update/",
        views.work_update_view,
        name="work_update_view",
    ),
    path(
        "work/<str:work_id>/student/<str:student_id>/remove/",
        views.remove_student_from_work_view,
        name="remove_student_from_work",
    ),
]
