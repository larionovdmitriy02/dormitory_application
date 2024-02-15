from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from dormitory.models import Dormitory
from student.models import Student
from news.models import News


@login_required
def dashboard_main_page_view(request: HttpRequest) -> HttpResponse:
    dormitories = Dormitory.objects.all().order_by("pk")
    users = Student.objects.all().exclude(is_superuser=True)
    students = sorted(
        Student.objects.all().exclude(is_superuser=True),
        key=lambda student: student.get_all_points,
        reverse=True,
    )[:5]
    news = News.objects.all().order_by("-pk")[:5]
    administrative_points = 0
    activity_points = 0
    for user in users:
        if user.administrative_points:
            administrative_points += user.administrative_points
        if user.activity_points:
            activity_points += user.activity_points
    context = {
        "dormitories": dormitories,
        "administrative_points": administrative_points,
        "activity_points": activity_points,
        "all_points": administrative_points + activity_points,
        "news": news,
        "students": students,
    }
    return render(
        request=request,
        template_name="dashboard/dashboard_main_page.html",
        context=context,
    )


def custom_404(request: HttpRequest, exception) -> HttpResponse:
    return render(request=request, template_name="dashboard/404.html", status=404)
