from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField


class News(models.Model):
    title = models.CharField(
        verbose_name="Название", max_length=255, blank=False, null=False
    )
    content = RichTextUploadingField(verbose_name="Описание", null=True, blank=True)
    created_at = models.DateTimeField(verbose_name="Время создания", auto_now_add=True)
    updated_at = models.DateTimeField(
        verbose_name="Время последнего обновления", auto_now=True
    )

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"

    def __str__(self):
        return self.title
