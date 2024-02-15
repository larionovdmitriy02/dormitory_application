from django.db import models
from student.models import Student
from ckeditor_uploader.fields import RichTextUploadingField


class Work(models.Model):
    name = models.CharField(
        verbose_name="Название", blank=False, null=False, max_length=500
    )
    participants_count = models.IntegerField(
        verbose_name="Количество студентов", blank=False, null=False, default=1
    )
    participants = models.ManyToManyField(
        Student,
        verbose_name="Студенты",
        blank=True,
    )
    is_administrative_work = models.BooleanField(
        verbose_name="Административные работа", blank=True, null=True
    )
    is_activity_work = models.BooleanField(
        verbose_name="Работа ССО", blank=True, null=True
    )
    work_date = models.DateField(verbose_name="Дата работы", blank=False, null=False)
    start_time = models.TimeField(verbose_name="Начало работы", null=False, blank=False)
    end_time = models.TimeField(
        verbose_name="Окончание работы", null=False, blank=False
    )
    description = RichTextUploadingField(verbose_name="Описание", null=True, blank=True)
    administrative_points = models.IntegerField(
        verbose_name="Административные баллы", blank=True, null=True, default=0
    )
    activity_points = models.IntegerField(
        verbose_name="Баллы ССО", blank=True, null=True, default=0
    )
    is_active = models.BooleanField(verbose_name="Активно", default=True)

    class Meta:
        verbose_name = "Работа"
        verbose_name_plural = "Работы"

    def __str__(self):
        return self.name

    @property
    def get_available_seats(self):
        return int(self.participants_count) - int(self.participants.all().count())

    @property
    def is_seats_available(self):
        return int(self.participants_count) > int(self.participants.all().count())


class WorkHistory(models.Model):
    work_id = models.ForeignKey(
        Work,
        verbose_name="Работа",
        null=True,
        blank=True,
        related_name="work_history",
        on_delete=models.CASCADE,
    )
    student_id = models.ForeignKey(
        Student,
        verbose_name="Студент",
        null=True,
        blank=True,
        related_name="student_work_history",
        on_delete=models.CASCADE,
    )
    status = models.CharField(
        verbose_name="Статус", blank=True, null=True, max_length=500
    )
    is_active = models.BooleanField(verbose_name="Активно", blank=True, null=True)

    class Meta:
        verbose_name = "История работы"
        verbose_name_plural = "История работ"

    def __str__(self) -> str:
        return self.work_id.name
