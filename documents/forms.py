"""
Documents forms module.
"""
from django import forms

from .models import Document


class DocumentModelForm(forms.ModelForm):
    """Documents edit form."""

    class Meta:
        """Documents edit from widgets config."""

        model = Document
        fields = ["document", "description", "title"]
        widgets = {
            "document": forms.FileInput(attrs={"class": "form-control"}),
            "description": forms.TextInput(attrs={"class": "form-control"}),
            "title": forms.HiddenInput(),
        }

    def save(self, commit: bool = True) -> Document:
        """Save document method."""
        instance = super(DocumentModelForm, self).save(False)
        instance.title = instance.document.name
        if commit:
            instance.save()
        return instance
