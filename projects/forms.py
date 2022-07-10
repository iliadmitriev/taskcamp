"""
Projects forms module.
"""
from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Comment, Project, Task


class ProjectModelForm(forms.ModelForm):
    """Project model form for creating and updating."""

    class Meta:
        """Project model form config.

        Args:
            fields (list): list of included model fields
            widgets (dict): dict of used widgets for fields
        """

        model = Project
        fields = ["title", "description", "due_date", "is_closed"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control"}),
            "due_date": forms.DateInput(attrs={"class": "form-control"}),
            "is_closed": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class TaskModelForm(forms.ModelForm):
    """Task model form for creating and updating."""

    class Meta:
        """Task Model form config.

        Args:
            fields (list): list of included model fields
            widgets (dict): dict of used widgets for fields

        """

        model = Task
        fields = [
            "project",
            "title",
            "author",
            "assignee",
            "start",
            "end",
            "status",
            "description",
        ]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control"}),
            "start": forms.DateTimeInput(attrs={"class": "form-control"}),
            "end": forms.DateTimeInput(attrs={"class": "form-control"}),
            "status": forms.Select(attrs={"class": "form-select"}),
            "project": forms.Select(attrs={"class": "form-select"}),
            "author": forms.Select(attrs={"class": "form-select"}),
            "assignee": forms.Select(attrs={"class": "form-select"}),
        }


class CommentModelForm(forms.ModelForm):
    """Comment model form for creating and updating."""

    class Meta:
        """Comment model form config.

        Args:
            fields (list): list of included model fields
            widgets (dict): dict of used widgets for fields
        """

        model = Comment
        fields = ["description"]
        widgets = {
            "description": forms.Textarea(
                attrs={"class": "form-control", "rows": 8, "placeholder": _("Comment")}
            ),
        }
