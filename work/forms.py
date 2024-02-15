from django import forms
from .models import Work


class DashboardAdministrativeWorkCreateChangeForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control", "style": "color: #fff;"})
    )
    administrative_points = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={"class": "form-control", "style": "color: #fff;"}
        )
    )
    participants_count = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={"class": "form-control", "style": "color: #fff;"}
        )
    )
    work_date = forms.DateField(
        widget=forms.DateInput(
            attrs={"class": "form-control", "style": "color: #fff;", "type": "date"},
        ),
        input_formats=["%Y-%m-%d"],
    )
    start_time = forms.TimeField(
        widget=forms.TimeInput(
            attrs={"class": "form-control timepicker", "style": "color: #fff;"},
        ),
    )
    end_time = forms.TimeField(
        widget=forms.TimeInput(
            attrs={"class": "form-control timepicker", "style": "color: #fff;"},
        ),
    )

    def __init__(self, *args, **kwargs):
        super(DashboardAdministrativeWorkCreateChangeForm, self).__init__(
            *args, **kwargs
        )
        if self.instance.work_date is not None:
            self.initial["work_date"] = self.instance.work_date.isoformat()

    class Meta:
        model = Work
        fields = (
            "name",
            "participants_count",
            "description",
            "administrative_points",
            "work_date",
            "start_time",
            "end_time",
            "is_administrative_work",
        )


class DashboardActivityWorkCreateChangeForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control", "style": "color: #fff;"})
    )
    activity_points = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={"class": "form-control", "style": "color: #fff;"}
        )
    )
    participants_count = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={"class": "form-control", "style": "color: #fff;"}
        )
    )
    work_date = forms.DateField(
        widget=forms.DateInput(
            attrs={"class": "form-control", "style": "color: #fff;", "type": "date"},
        ),
        input_formats=["%Y-%m-%d"],
    )
    start_time = forms.TimeField(
        widget=forms.TimeInput(
            attrs={"class": "form-control timepicker", "style": "color: #fff;"},
        ),
    )
    end_time = forms.TimeField(
        widget=forms.TimeInput(
            attrs={"class": "form-control timepicker", "style": "color: #fff;"},
        ),
    )

    def __init__(self, *args, **kwargs):
        super(DashboardActivityWorkCreateChangeForm, self).__init__(*args, **kwargs)
        if self.instance.work_date is not None:
            self.initial["work_date"] = self.instance.work_date.isoformat()

    class Meta:
        model = Work
        fields = (
            "name",
            "participants_count",
            "description",
            "activity_points",
            "work_date",
            "start_time",
            "end_time",
            "is_activity_work",
        )
