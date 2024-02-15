from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Work, WorkHistory
from .forms import (
    DashboardAdministrativeWorkCreateChangeForm,
    DashboardActivityWorkCreateChangeForm,
)
from student.models import Student


@login_required
def work_student_all_end(request: HttpRequest, work_id: str) -> HttpResponse:
    if not request.user.is_superuser:
        messages.warning(request=request, message="Вы не можете этого сделать")
        return redirect("dashboard_main_page_view")
    work = get_object_or_404(Work, pk=work_id)
    for student in work.participants.all():
        work_history = get_object_or_404(
            WorkHistory, student_id=student, work_id=work_id, is_active=True
        )
        if work.is_administrative_work:
            student.administrative_points += int(work.administrative_points)
            work_history.status = f"Работа завершена успешно. Баллов получено: {work.administrative_points} из {work.administrative_points}"
        else:
            student.activity_points += int(work.activity_points)
            work_history.status = f"Работа завершена успешно. Баллов получено: {work.activity_points} из {work.activity_points}"
        work_history.is_active = False
        work_history.save()
        student.save()
        work.participants.remove(student)
    work.is_active = False
    work.save()
    messages.success(request=request, message="Вы успешно обработали всех студентов")
    return redirect("work_list_view")


@login_required
def work_student_ready_view(
    request: HttpRequest, student_id: str, work_id: str
) -> HttpResponse:
    if not request.user.is_superuser:
        messages.warning(request=request, message="Вы не можете этого сделать")
        return redirect("dashboard_main_page_view")
    work = get_object_or_404(Work, pk=work_id)
    student = get_object_or_404(Student, pk=student_id)
    work_history = get_object_or_404(
        WorkHistory, student_id=student_id, work_id=work_id, is_active=True
    )
    if work.is_administrative_work:
        student.administrative_points += int(request.POST.get("points"))
        work_history.status = f"Работа завершена успешно. Баллов получено: {request.POST.get('points')} из {work.administrative_points}"
    else:
        student.activity_points += int(request.POST.get("points"))
        work_history.status = f"Работа завершена успешно. Баллов получено: {request.POST.get('points')} из {work.activity_points}"
    work_history.is_active = False
    work_history.save()
    student.save()
    work.participants.remove(student)
    if len(work.participants.all()) == 0:
        work.is_active = False
        work.save()
        return redirect("work_list_view")
    messages.success(request=request, message="Вы успешно обработали студента")
    return redirect("work_detail_view", work_id=work_id)


@login_required
def work_finish_view(request: HttpRequest, work_id: str) -> HttpResponse:
    if not request.user.is_superuser:
        messages.warning(request=request, message="Вы не можете этого сделать")
        return redirect("dashboard_main_page_view")
    work = get_object_or_404(Work, pk=work_id)
    work.is_active = False
    work.save()
    messages.success(request=request, message="Работа успешно завершена")
    return redirect("work_list_view")


@login_required
def add_student_to_work_view(
    request: HttpRequest, student_id: str, work_id: str
) -> HttpResponse:
    work = get_object_or_404(Work, pk=work_id)
    if work.is_seats_available:
        student = get_object_or_404(Student, pk=student_id)
        work.participants.add(student)
        work_history = WorkHistory(work_id=work, student_id=student, is_active=True)
        work_history.save()
        messages.success(
            request=request, message="Студент был успешно добавлен к работе"
        )
        return redirect("work_detail_view", work_id=work_id)
    else:
        messages.warning(request=request, message="Вы не можете добавить еще студентов")
        return redirect("work_detail_view", work_id=work_id)


@login_required
def work_student_list_view(request: HttpRequest, work_id: str) -> HttpResponse:
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
        students = Student.objects.all()
    context_students = []
    work = get_object_or_404(Work, pk=work_id)
    for student in students.exclude(is_superuser=True):
        if student not in work.participants.all():
            context_students.append(student)
    context = {
        "students": context_students,
        "work_id": work_id,
    }
    return render(
        request=request, template_name="work/student_list_page.html", context=context
    )


@login_required
def remove_student_from_work_view(
    request: HttpRequest, work_id: str, student_id: str
) -> HttpResponse:
    if not request.user.is_superuser:
        messages.warning(request=request, message="Вы не можете этого сделать")
        return redirect("dashboard_main_page_view")
    work = get_object_or_404(Work, pk=work_id)
    student = get_object_or_404(Student, pk=student_id)
    work_history = get_object_or_404(
        WorkHistory, student_id=student_id, work_id=work_id, is_active=True
    )
    work_history.is_active = False
    work_history.status = f"Вас удалили. Причина: {request.POST.get('reason')}"
    work_history.save()
    work.participants.remove(student)
    messages.success(request=request, message="Вы успешно удалили студента из работы")
    return redirect("work_detail_view", work_id=work_id)


@login_required
def work_take_part_view(request: HttpRequest, work_id: str) -> HttpResponse:
    work = get_object_or_404(Work, pk=work_id)
    if (
        len(work.participants.all()) < work.participants_count
        and request.user not in work.participants.all()
    ):
        work.participants.add(request.user)
        work_history = WorkHistory(
            work_id=work, student_id=request.user, is_active=True
        )
        work_history.save()
        messages.success(request=request, message="Вы успешно приняли работу")
        return redirect("work_list_view")
    else:
        messages.warning(request=request, message="Вы не можете этого сделать")
        return redirect("work_list_view")


@login_required
def work_administrative_create_view(request: HttpRequest) -> HttpResponse:
    if not request.user.is_superuser:
        messages.warning(request=request, message="Вы не можете этого сделать")
        return redirect("dashboard_main_page_view")
    context = {}
    if request.POST:
        form = DashboardAdministrativeWorkCreateChangeForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.is_administrative_work = True
            form.save()
            messages.success(request=request, message="Вы успешно создали работу")
            return redirect("work_list_view")
    else:
        form = DashboardAdministrativeWorkCreateChangeForm()
    context["form"] = form
    return render(
        request=request,
        template_name="work/work_administrative_create_page.html",
        context=context,
    )


@login_required
def work_activity_create_view(request: HttpRequest) -> HttpResponse:
    if not request.user.is_superuser:
        messages.warning(request=request, message="Вы не можете этого сделать")
        return redirect("dashboard_main_page_view")
    context = {}
    if request.POST:
        form = DashboardActivityWorkCreateChangeForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.is_activity_work = True
            form.save()
            messages.success(request=request, message="Вы успешно создали работу")
            return redirect("work_list_view")
    else:
        form = DashboardActivityWorkCreateChangeForm()
    context["form"] = form
    return render(
        request=request,
        template_name="work/work_activity_create_page.html",
        context=context,
    )


@login_required
def work_update_view(request: HttpRequest, work_id: str) -> HttpResponse:
    if not request.user.is_superuser:
        messages.warning(request=request, message="Вы не можете этого сделать")
        return redirect("dashboard_main_page_view")
    work = get_object_or_404(Work, pk=work_id)
    context = {
        "work": work,
    }
    if work.is_administrative_work:
        if request.POST:
            form = DashboardAdministrativeWorkCreateChangeForm(
                request.POST, request.FILES, instance=work
            )
            if form.is_valid():
                form.instance.is_administrative_work = True
                form.save()
                messages.success(
                    request=request, message="Информация была успешно обновлена"
                )
                return redirect("work_detail_view", work_id=work.pk)
        else:
            form = DashboardAdministrativeWorkCreateChangeForm(instance=work)
        context["form"] = form
    else:
        if request.POST:
            form = DashboardActivityWorkCreateChangeForm(
                request.POST, request.FILES, instance=work
            )
            if form.is_valid():
                form.instance.is_activity_work = True
                form.save()
                messages.success(
                    request=request, message="Информация была успешно обновлена"
                )
                return redirect("work_detail_view", work_id=work.pk)
        else:
            form = DashboardActivityWorkCreateChangeForm(instance=work)
        context["form"] = form
    return render(
        request=request,
        template_name="work/work_update_page.html",
        context=context,
    )


@login_required
def work_list_view(request: HttpRequest) -> HttpResponse:
    works = Work.objects.filter(is_active=True)
    context = {
        "works": works,
    }
    return render(
        request=request, template_name="work/work_list_page.html", context=context
    )


@login_required
def work_detail_view(request: HttpRequest, work_id: str) -> HttpResponse:
    context = {}
    work = get_object_or_404(Work, pk=work_id)
    context["work"] = work
    return render(
        request=request,
        template_name="work/work_detail_page.html",
        context=context,
    )
