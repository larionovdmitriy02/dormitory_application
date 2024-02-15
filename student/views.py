from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Student, StudentDocument
from .forms import (
    StudentDashboardChangeForm,
    StudentAuthenticationForm,
    StudentDashboardCreationForm,
    StudentDocumentUploadForm,
)
from django.contrib import messages
from work.models import WorkHistory


@login_required
def student_document_delete_view(
    request: HttpRequest, student_id: str, file_id: str
) -> HttpResponse:
    file = get_object_or_404(StudentDocument, pk=file_id)
    file.delete()
    messages.success(request=request, message="Файл был успешно удален")
    return redirect("student_detail_view", student_id=student_id)


@login_required
def student_download_document_view(request: HttpRequest, file_id: str) -> HttpResponse:
    file_obj = get_object_or_404(StudentDocument, pk=file_id)
    file_path = file_obj.file_content.path
    with open(file_path, "rb") as file:
        response = HttpResponse(file.read(), content_type="application/force-download")
        response[
            "Content-Disposition"
        ] = f"attachment; filename={file_obj.file_content.name}"
        return response


@login_required
def student_upload_document_view(request: HttpRequest, student_id: str) -> HttpResponse:
    student_document = StudentDocument(
        student_id=get_object_or_404(Student, pk=student_id),
        file_content=request.FILES.get("file"),
    )
    student_document.save()
    messages.success(request=request, message="Файл был успешно загружен")
    return redirect("student_detail_view", student_id=student_id)


@login_required
def student_work_list_view(request: HttpRequest, student_id: str) -> HttpResponse:
    work_history_nonactive = WorkHistory.objects.filter(
        student_id=student_id, is_active=False
    ).order_by("-pk")
    context = {"work_history_nonactive": work_history_nonactive}
    return render(
        request=request,
        template_name="student/student_work_list_page.html",
        context=context,
    )


@login_required
def student_delete_view(request: HttpRequest, student_id: str) -> HttpResponse:
    if not request.user.is_superuser:
        messages.warning(request=request, message="Вы не можете этого сделать")
        return redirect("dashboard_main_page_view")
    student = get_object_or_404(Student, pk=student_id)
    student.delete()
    messages.success(request=request, message="Студент успешно удален")
    return redirect("student_list_view")


@login_required
def student_list_view(request: HttpRequest) -> HttpResponse:
    search_student = request.GET.get("search")
    if search_student:
        students = None
        search_student = search_student.split(" ")
        for item in search_student:
            students = Student.objects.filter(
                Q(first_name__icontains=item) | Q(second_name__icontains=item)
            )
            if students is not None:
                break
    else:
        students = Student.objects.all().exclude(is_superuser=True)
    context = {
        "students": students,
    }
    return render(
        request=request,
        template_name="student/student_list_page.html",
        context=context,
    )


@login_required
def student_rating_view(request: HttpRequest) -> HttpResponse:
    students = sorted(
        Student.objects.all().exclude(is_superuser=True),
        key=lambda student: student.get_all_points,
        reverse=True,
    )
    context = {"students": students}
    return render(
        request=request,
        template_name="student/student_rating_page.html",
        context=context,
    )


@login_required
def student_create_view(request: HttpRequest) -> HttpResponse:
    if not request.user.is_superuser:
        messages.warning(request=request, message="Вы не можете этого сделать")
        return redirect("dashboard_main_page_view")
    context = {}
    if request.POST:
        form = StudentDashboardCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request=request, message="Вы успешно создали студента")
            return redirect("dashboard_main_page_view")
    else:
        form = StudentDashboardCreationForm(
            initial={"administrative_points": 0, "activity_points": 0}
        )
    context["form"] = form
    return render(
        request=request,
        template_name="student/student_create_page.html",
        context=context,
    )


def student_login_view(request: HttpRequest) -> HttpResponse:
    context = {}
    student = request.user
    if student.is_authenticated:
        return redirect("dashboard_main_page_view")
    if request.POST:
        form = StudentAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST.get("email")
            password = request.POST.get("password")
            student = authenticate(email=email, password=password)
            if student:
                login(request=request, user=student)
                messages.success(request=request, message="Вы успешно вошли")
                return redirect("dashboard_main_page_view")
    else:
        form = StudentAuthenticationForm()
    context["form"] = form
    return render(
        request=request,
        template_name="student/student_login_page.html",
        context=context,
    )


@login_required
def student_logout_view(request: HttpRequest) -> HttpResponse:
    logout(request=request)
    return redirect("dashboard_main_page_view")


@login_required
def student_detail_view(request: HttpRequest, student_id: str) -> HttpResponse:
    student = get_object_or_404(Student, pk=student_id)
    documents = StudentDocument.objects.filter(student_id=student_id)
    work_history_active = WorkHistory.objects.filter(
        student_id=student_id, is_active=True
    ).order_by("-pk")
    work_history_nonactive = WorkHistory.objects.filter(
        student_id=student_id, is_active=False
    ).order_by("-pk")[:5]
    context = {
        "student": student,
        "work_history_active": work_history_active,
        "work_history_nonactive": work_history_nonactive,
        "documents": documents,
    }
    return render(
        request=request,
        template_name="student/student_detail_page.html",
        context=context,
    )


@login_required
def student_update_view(request: HttpRequest, student_id: str) -> HttpResponse:
    if not request.user.is_superuser:
        messages.warning(request=request, message="Вы не можете этого сделать")
        return redirect("dashboard_main_page_view")
    student = get_object_or_404(Student, pk=student_id)
    context = {
        "student": student,
    }
    if request.POST:
        form = StudentDashboardChangeForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            messages.success(
                request=request, message="Информация была успешно обновлена"
            )
            return redirect("student_detail_view", student_id=student_id)
    else:
        form = StudentDashboardChangeForm(instance=student)
    context["form"] = form
    return render(
        request=request,
        template_name="student/student_update_page.html",
        context=context,
    )
