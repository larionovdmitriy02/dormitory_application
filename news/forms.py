from django import forms
from .models import News


class NewsCreateUpdateForm(forms.ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control", "style": "color: #fff;"})
    )

    class Meta:
        model = News
        fields = ["title", "content"]
