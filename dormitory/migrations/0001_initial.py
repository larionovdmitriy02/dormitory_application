# Generated by Django 4.2.8 on 2023-12-16 16:19

import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Dormitory",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        db_index=True,
                        max_length=255,
                        unique=True,
                        verbose_name="Название",
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        upload_to="dormitory_images", verbose_name="Изображение"
                    ),
                ),
                (
                    "description",
                    ckeditor_uploader.fields.RichTextUploadingField(
                        blank=True, null=True, verbose_name="Описание"
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Время создания"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        auto_now=True, verbose_name="Время последнего обновления"
                    ),
                ),
            ],
            options={
                "verbose_name": "Общежитие",
                "verbose_name_plural": "Общежития",
            },
        ),
    ]
