from django.contrib import admin
from .models import Project, Task, Comment


class ProjectAdmin(admin.ModelAdmin):
    readonly_fields = ['id']
    fields = ['id', 'title', 'description', 'due_date', 'is_closed']
    list_display = ['id', 'title', 'description', 'due_date', 'is_closed']
    search_fields = ['title', 'description']
    list_filter = ['due_date', 'is_closed']


class TaskAdmin(admin.ModelAdmin):
    list_select_related = True
    readonly_fields = ['id']
    fields = [
        'id', 'project', 'title', 'description', 'start', 'end',
        'author', 'assignee', 'status'
    ]
    list_display = [
        'id', 'title', 'project', 'description', 'start', 'end',
        'author', 'assignee', 'status'
    ]
    search_fields = ['title', 'description']
    list_filter = ['status']
    raw_id_fields = ['project', 'author', 'assignee']


class CommentAdmin(admin.ModelAdmin):
    list_select_related = True
    readonly_fields = ['id', 'created']
    fields = ['id', 'created', 'task', 'description']
    raw_id_fields = ['task']
    search_fields = ['description']
    list_display = ['id', 'task', 'created', 'description']


admin.site.register(Project, ProjectAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Comment, CommentAdmin)
