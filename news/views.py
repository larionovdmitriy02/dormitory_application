from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from .models import News
from .forms import NewsCreateUpdateForm
from django.contrib import messages


@login_required
def news_delete_view(request: HttpRequest, news_id: str) -> HttpResponse:
    if not request.user.is_superuser:
        messages.warning(request=request, message="Вы не можете этого сделать")
        return redirect("dashboard_main_page_view")
    news = get_object_or_404(News, pk=news_id)
    news.delete()
    messages.success(request=request, message="Новость успешно удалена")
    return redirect("news_list_view")


@login_required
def news_create_view(request: HttpRequest) -> HttpResponse:
    if not request.user.is_superuser:
        messages.warning(request=request, message="Вы не можете этого сделать")
        return redirect("dashboard_main_page_view")
    context = {}
    if request.POST:
        form = NewsCreateUpdateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request=request, message="Новость успешно создана")
            return redirect("news_list_view")
    else:
        form = NewsCreateUpdateForm()
    context["form"] = form
    return render(
        request=request, template_name="news/news_create_page.html", context=context
    )


@login_required
def news_update_view(request: HttpRequest, news_id: str) -> HttpResponse:
    if not request.user.is_superuser:
        messages.warning(request=request, message="Вы не можете этого сделать")
        return redirect("dashboard_main_page_view")
    news = get_object_or_404(News, pk=news_id)
    context = {
        "news": news,
    }
    if request.POST:
        form = NewsCreateUpdateForm(request.POST, request.FILES, instance=news)
        if form.is_valid():
            form.save()
            messages.success(request=request, message="Новость успешно обновлена")
            return redirect("news_detail_view", news_id=news_id)
    else:
        form = NewsCreateUpdateForm(instance=news)
    context["form"] = form
    return render(
        request=request, template_name="news/news_update_page.html", context=context
    )


@login_required
def news_list_view(request: HttpRequest) -> HttpResponse:
    news = News.objects.all().order_by("-created_at")
    context = {
        "news": news,
    }
    return render(
        request=request, template_name="news/news_list_page.html", context=context
    )


@login_required
def news_detail_view(request: HttpRequest, news_id: str) -> HttpResponse:
    news = get_object_or_404(News, pk=news_id)
    context = {"news": news}
    return render(
        request=request, template_name="news/news_detail_page.html", context=context
    )
