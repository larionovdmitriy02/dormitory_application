from django import forms
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from .models import Student, StudentDocument
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from dormitory.models import Dormitory


class StudentDocumentUploadForm(forms.ModelForm):
    class Meta:
        model = StudentDocument
        fields = ["file_content"]


class StudentAuthenticationForm(forms.ModelForm):
    email = forms.EmailField(
        label="",
        max_length=255,
        widget=forms.EmailInput(
            attrs={
                "class": "form-control mb-3",
                "placeholder": "Email",
                "style": "color: white; font-size: 17px; padding: 20px;",
            }
        ),
    )

    password = forms.CharField(
        label="",
        max_length=255,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control mb-3",
                "placeholder": "Пароль",
                "style": "color: white; font-size: 17px; padding: 20px;",
            }
        ),
    )

    class Meta:
        model = Student
        fields = ("email", "password")

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data.get("email")
            password = self.cleaned_data.get("password")
            if not authenticate(email=email, password=password):
                raise ValidationError("Неправильный логин или пароль. Попробуйте снова")


class StudentCreationForm(forms.ModelForm):
    password = forms.CharField(
        label="Пароль", max_length=255, widget=forms.PasswordInput
    )

    class Meta:
        model = Student
        fields = [
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
        ]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        try:
            student = Student.objects.get(email=email)
        except Exception as e:
            return email
        raise ValidationError("Студент с таким email уже существует")

    def save(self, commit=True):
        student = super().save(commit=False)
        student.set_password(raw_password=self.cleaned_data.get("password"))
        if commit:
            student.save()
        return student


class StudentDashboardCreationForm(forms.ModelForm):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control", "style": "color: #fff;"})
    )
    second_name = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control", "style": "color: #fff;"})
    )
    third_name = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control", "style": "color: #fff;"})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"class": "form-control", "style": "color: #fff;"}
        )
    )
    phone_number = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "style": "color: #fff;"}
        ),
        required=False,
    )
    administrative_points = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={"class": "form-control", "style": "color: #fff;"}
        ),
        required=False,
    )
    activity_points = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={"class": "form-control", "style": "color: #fff;"}
        ),
        required=False,
    )
    dormitory = forms.ModelChoiceField(
        queryset=Dormitory.objects.all(),
        widget=forms.Select(attrs={"class": "form-control", "style": "color: #fff;"}),
    )

    password = forms.CharField(
        label="Пароль",
        max_length=255,
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "style": "color: #fff;"}
        ),
    )

    class Meta:
        model = Student
        fields = [
            "email",
            "first_name",
            "second_name",
            "third_name",
            "dormitory",
            "administrative_points",
            "activity_points",
            "phone_number",
            "profile_image",
            "password",
        ]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        try:
            student = Student.objects.get(email=email)
        except Exception as e:
            return email
        raise ValidationError("Студент с таким email уже существует")

    def clean_password(self):
        password = self.cleaned_data.get("password")
        if len(password) < 8:
            raise ValidationError("Пароль должен состоять из 8 или более символов")
        return password

    def save(self, commit=True):
        student = super().save(commit=False)
        student.set_password(raw_password=self.cleaned_data.get("password"))
        if commit:
            student.save()
        return student


class StudentChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(label="Пароль")

    class Meta:
        model = Student
        fields = [
            "email",
            "first_name",
            "second_name",
            "dormitory",
            "third_name",
            "administrative_points",
            "activity_points",
            "phone_number",
            "status",
            "profile_image",
        ]


class StudentDashboardChangeForm(forms.ModelForm):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control", "style": "color: #fff;"})
    )
    second_name = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control", "style": "color: #fff;"})
    )
    third_name = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control", "style": "color: #fff;"})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"class": "form-control", "style": "color: #fff;"}
        )
    )
    phone_number = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "style": "color: #fff;"}
        ),
        required=False,
    )
    administrative_points = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={"class": "form-control", "style": "color: #fff;"}
        ),
        required=False,
    )
    activity_points = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={"class": "form-control", "style": "color: #fff;"}
        ),
        required=False,
    )
    dormitory = forms.ModelChoiceField(
        queryset=Dormitory.objects.all(),
        widget=forms.Select(attrs={"class": "form-control", "style": "color: #fff;"}),
    )
    status = forms.ChoiceField(
        widget=forms.Select(attrs={"class": "form-control", "style": "color: #fff;"}),
        choices=(
            ("Золото", "Золото"),
            ("Серебро", "Серебро"),
            ("Бронза", "Бронза"),
        ),
    )

    class Meta:
        model = Student
        fields = [
            "email",
            "first_name",
            "second_name",
            "dormitory",
            "third_name",
            "administrative_points",
            "activity_points",
            "phone_number",
            "status",
            "profile_image",
        ]
