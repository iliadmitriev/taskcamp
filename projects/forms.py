from django import forms
from .models import Project, Task, Comment


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
            'project', 'title', 'author', 'assignee', 'start', 'end',
            'status', 'description'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'start': forms.DateTimeInput(attrs={'class': 'form-control'}),
            'end': forms.DateTimeInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'project': forms.Select(attrs={'class': 'form-select'}),
            'author': forms.Select(attrs={'class': 'form-select'}),
            'assignee': forms.Select(attrs={'class': 'form-select'}),

        }


class CommentModelForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            'description'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }
