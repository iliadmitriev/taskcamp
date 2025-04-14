"""Employee forms module."""

from django import forms

from .models import Employee


class EmployeeModelForm(forms.ModelForm):
    """Employee create and edit model form."""

    class Meta:
        """Employee model form config."""

        model = Employee
        fields = ["firstname", "surname", "birthdate", "email"]
        widgets = {
            "firstname": forms.TextInput(attrs={"class": "form-control"}),
            "surname": forms.TextInput(attrs={"class": "form-control"}),
            "birthdate": forms.DateInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
        }
