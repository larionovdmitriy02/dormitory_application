from django.contrib import admin
from .models import Dormitory


class DormitoryAdmin(admin.ModelAdmin):
    list_display = ("name", "get_students_count", "image_tag")
    search_fields = ("name",)
    list_filter = ("name",)

    fieldsets = [
        (
            None,
            {
                "fields": [
                    "name",
                    "image",
                    "description",
                    "created_at",
                    "updated_at",
                ]
            },
        ),
    ]

    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": [
                    "name",
                    "image",
                    "description",
                ],
            },
        ),
    ]

    readonly_fields = ["created_at", "updated_at"]
    filter_horizontal = []


admin.site.register(Dormitory, DormitoryAdmin)
