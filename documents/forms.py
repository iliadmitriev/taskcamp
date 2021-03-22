from django import forms
from .models import Document


class DocumentModeForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['document', 'description']
        widgets = {
            'document': forms.FileInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'})
        }
