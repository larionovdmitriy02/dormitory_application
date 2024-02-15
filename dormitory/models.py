from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.safestring import mark_safe


class Dormitory(models.Model):
    name = models.CharField(
        verbose_name="Название",
        max_length=255,
        unique=True,
        db_index=True,
        blank=False,
        null=False,
    )
    image = models.ImageField(
        verbose_name="Изображение",
        upload_to="dormitory_images",
        null=False,
        blank=False,
    )
    description = RichTextUploadingField(verbose_name="Описание", null=True, blank=True)
    created_at = models.DateTimeField(verbose_name="Время создания", auto_now_add=True)
    updated_at = models.DateTimeField(
        verbose_name="Время последнего обновления", auto_now=True
    )

    class Meta:
        verbose_name = "Общежитие"
        verbose_name_plural = "Общежития"

    def __str__(self):
        return self.name

    def get_students_count(self):
        return self.students.all().count()

    get_students_count.short_description = "Количество проживающих студентов "

    def image_tag(self):
        return mark_safe(
            '<img src="%s" width="100px" height="100px" />' % (self.image.url)
        )

    image_tag.short_description = "Изображение"

    # @@property
    # def image_preview(self):
    #     return
