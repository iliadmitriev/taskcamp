from django import forms
from .models import Document


class DocumentModeForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['document', 'description', 'title']
        widgets = {
            'document': forms.FileInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'title': forms.HiddenInput()
        }

    def save(self, commit=True):
        instance = super(DocumentModeForm, self).save(False)
        instance.title = instance.document.name
        if commit:
            instance.save()
        return instance
