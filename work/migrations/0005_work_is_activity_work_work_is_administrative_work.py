# Generated by Django 4.2.8 on 2023-12-23 10:48

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("work", "0004_remove_work_nonactive_participants_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="work",
            name="is_activity_work",
            field=models.BooleanField(blank=True, null=True, verbose_name="Работа ССО"),
        ),
        migrations.AddField(
            model_name="work",
            name="is_administrative_work",
            field=models.BooleanField(
                blank=True, null=True, verbose_name="Административные работа"
            ),
        ),
    ]
