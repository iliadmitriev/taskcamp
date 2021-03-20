from django import forms
from .models import Project, Task


class ProjectModelForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'due_date', 'is_closed']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'due_date': forms.DateInput(attrs={'class': 'form-control'}),
            'is_closed': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class TaskModelForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            'project', 'title', 'description',
            'author', 'assignee', 'start', 'end',
            'status'
        ]
