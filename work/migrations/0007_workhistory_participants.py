# Generated by Django 4.2.8 on 2023-12-23 13:53

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("work", "0006_alter_workhistory_options_workhistory_is_active"),
    ]

    operations = [
        migrations.AddField(
            model_name="workhistory",
            name="participants",
            field=models.ManyToManyField(
                blank=True, to=settings.AUTH_USER_MODEL, verbose_name="Студенты"
            ),
        ),
    ]
