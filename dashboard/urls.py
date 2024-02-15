from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.dashboard_main_page_view, name="dashboard_main_page_view"),
    path("", include("dormitory.urls")),
    path("", include("student.urls")),
    path("", include("news.urls")),
    path("", include("work.urls")),
]