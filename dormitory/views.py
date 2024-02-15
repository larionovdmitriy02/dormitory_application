from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Dormitory
from .forms import DormitoryUpdateForm
from django.contrib import messages


@login_required
def dormitory_delete_view(request: HttpRequest, dormitory_id: str) -> HttpResponse:
    if not request.user.is_superuser:
        messages.warning(request=request, message="Вы не можете этого сделать")
        return redirect("dashboard_main_page_view")
    dormitory = get_object_or_404(Dormitory, pk=dormitory_id)
    dormitory.delete()
    messages.success(request=request, message="Общежитие успешно удалено")
    return redirect("dormitory_list_view")


@login_required
def dormitory_create_view(request: HttpRequest) -> HttpResponse:
    if not request.user.is_superuser:
        messages.warning(request=request, message="Вы не можете этого сделать")
        return redirect("dashboard_main_page_view")
    context = {}
    if request.POST:
        form = DormitoryUpdateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request=request, message="Общежитие успешно создано")
            return redirect("dormitory_list_view")
    else:
        form = DormitoryUpdateForm()
    context["form"] = form
    return render(
        request=request,
        template_name="dormitory/dormitory_create_page.html",
        context=context,
    )


@login_required
def dormitory_detail_view(request: HttpRequest, dormitory_id: str) -> HttpResponse:
    dormitory = get_object_or_404(Dormitory, pk=dormitory_id)
    context = {
        "dormitory": dormitory,
    }
    return render(
        request=request,
        template_name="dormitory/dormitory_detail_page.html",
        context=context,
    )


@login_required
def dormitory_list_view(request: HttpRequest) -> HttpResponse:
    dormitories = Dormitory.objects.all().order_by("pk")
    context = {"dormitories": dormitories}
    return render(
        request=request,
        template_name="dormitory/dormitory_list_page.html",
        context=context,
    )


@login_required
def dormitory_update_view(request: HttpRequest, dormitory_id: str) -> HttpResponse:
    if not request.user.is_superuser:
        messages.warning(request=request, message="Вы не можете этого сделать")
        return redirect("dashboard_main_page_view")
    dormitory = get_object_or_404(Dormitory, pk=dormitory_id)
    context = {
        "dormitory": dormitory,
    }
    if request.POST:
        form = DormitoryUpdateForm(request.POST, request.FILES, instance=dormitory)
        if form.is_valid():
            form.save()
            messages.success(request=request, message="Общежитие успешно обновлено")
            return redirect("dormitory_detail_view", dormitory_id=dormitory_id)
    else:
        form = DormitoryUpdateForm(instance=dormitory)
    context["form"] = form
    return render(
        request=request,
        template_name="dormitory/dormitory_update_page.html",
        context=context,
    )
