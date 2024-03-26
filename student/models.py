from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from dormitory.models import Dormitory
from django.dispatch import receiver
from django.db.models.signals import pre_save


class StudentManager(BaseUserManager):
    def create_user(self, email, first_name, second_name, third_name, password=None):
        if not email:
            raise ValueError("Студенты должны иметь Email адрес")
        if not first_name:
            raise ValueError("Студенты должны иметь имя")
        if not second_name:
            raise ValueError("Студенты должны иметь фамилию")
        if not third_name:
            raise ValueError("Студенты должны иметь отчество")
        student = self.model(
            email=self.normalize_email(email=email),
            first_name=first_name,
            second_name=second_name,
            third_name=third_name,
        )
        student.set_password(raw_password=password)
        student.save(using=self._db)
        return student

    def create_superuser(
        self, email, first_name, second_name, third_name, password=None
    ):
        student = self.create_user(
            email=email,
            first_name=first_name,
            second_name=second_name,
            third_name=third_name,
            password=password,
        )
        student.is_superuser = True
        student.is_student = False
        student.save(using=self._db)
        return student


class Student(AbstractBaseUser):
    STATUS_CHOICES = (
        ("Золото", "Золото"),
        ("Серебро", "Серебро"),
        ("Бронза", "Бронза"),
    )

    email = models.EmailField(
        verbose_name="Email",
        max_length=255,
        unique=True,
        db_index=True,
        null=False,
        blank=False,
    )
    first_name = models.CharField(
        verbose_name="Имя", max_length=255, null=False, blank=False
    )
    second_name = models.CharField(
        verbose_name="Фамилия", max_length=255, null=False, blank=False
    )
    third_name = models.CharField(
        verbose_name="Отчество", max_length=255, null=False, blank=False
    )
    dormitory = models.ForeignKey(
        Dormitory,
        related_name="students",
        on_delete=models.CASCADE,
        verbose_name="Общежитие",
        null=True,
        blank=True,
    )
    administrative_points = models.IntegerField(
        verbose_name="Административные баллы", default=0, null=True, blank=True
    )
    activity_points = models.IntegerField(
        verbose_name="Баллы ССО", default=0, null=True, blank=True
    )

    created_at = models.DateTimeField(verbose_name="Время создания", auto_now_add=True)
    updated_at = models.DateTimeField(
        verbose_name="Время последнего обновления", auto_now=True
    )
    phone_number = models.CharField(
        verbose_name="Телефон", blank=True, null=True, max_length=12
    )
    status = models.CharField(
        verbose_name="Статус", choices=STATUS_CHOICES, default="Бронза"
    )
    profile_image = models.ImageField(
        verbose_name="Фото", upload_to="student_profile_images", null=True, blank=True
    )

    is_student = models.BooleanField(verbose_name="Студент", default=True)
    is_superuser = models.BooleanField(verbose_name="Админ", default=False)

    objects = StudentManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "second_name", "third_name"]

    class Meta:
        verbose_name = "Студент"
        verbose_name_plural = "Студенты"

    def __str__(self):
        return f"{self.second_name} {self.first_name} {self.third_name}"

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_superuser

    @property
    def get_all_points(self):
        administrative_points = (
            self.administrative_points if self.administrative_points is not None else 0
        )
        activity_points = (
            self.activity_points if self.activity_points is not None else 0
        )
        return administrative_points + activity_points

    @property
    def get_short_name(self):
        return f"{self.second_name} {self.first_name}"


@receiver(pre_save, sender=Student)
def update_student_status(sender, instance, **kwargs):
    if int(instance.get_all_points) < 100:
        instance.status = "Бронза"
    elif 100 <= int(instance.get_all_points) <= 200:
        instance.status = "Серебро"
    else:
        instance.status = "Золото"


class StudentDocument(models.Model):
    student_id = models.ForeignKey(
        Student,
        verbose_name="Студент",
        blank=True,
        null=True,
        related_name="documents",
        on_delete=models.CASCADE,
    )
    file_content = models.FileField(upload_to="documents/", verbose_name="Документ")

    def __str__(self) -> str:
        return self.file_content.name

    class Meta:
        verbose_name = "Документ"
        verbose_name_plural = "Документы"
