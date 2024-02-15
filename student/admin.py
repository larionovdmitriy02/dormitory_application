from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from .models import Student, StudentDocument
from .forms import StudentCreationForm, StudentChangeForm


class StudentAdmin(UserAdmin):
    form = StudentChangeForm
    add_form = StudentCreationForm

    list_display = [
        "email",
        "first_name",
        "second_name",
        "third_name",
    ]
    list_filter = ["is_student", "is_superuser"]
    fieldsets = [
        (None, {"fields": ["email", "password"]}),
        (
            "Личная информация",
            {
                "fields": [
                    "first_name",
                    "second_name",
                    "third_name",
                    "dormitory",
                    "administrative_points",
                    "activity_points",
                    "phone_number",
                    "status",
                    "profile_image",
                ]
            },
        ),
        ("Права доступа", {"fields": ["is_student", "is_superuser"]}),
        ("Техническая информация", {"fields": ["created_at", "updated_at"]}),
    ]
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": [
                    "email",
                    "first_name",
                    "second_name",
                    "third_name",
                    "dormitory",
                    "administrative_points",
                    "activity_points",
                    "phone_number",
                    "status",
                    "profile_image",
                    "password",
                ],
            },
        ),
    ]
    search_fields = ["email"]
    ordering = ["email"]
    readonly_fields = ["created_at", "updated_at"]
    filter_horizontal = []


admin.site.register(Student, StudentAdmin)
admin.site.register(StudentDocument)

admin.site.unregister(Group)
