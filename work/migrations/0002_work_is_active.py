# Generated by Django 4.2.8 on 2023-12-18 17:59

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("work", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="work",
            name="is_active",
            field=models.BooleanField(default=True, verbose_name="Активно"),
        ),
    ]
