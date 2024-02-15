from django import forms
from .models import Dormitory


class DormitoryUpdateForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control", "style": "color: #fff;"})
    )

    class Meta:
        model = Dormitory
        fields = ["name", "image", "description"]
