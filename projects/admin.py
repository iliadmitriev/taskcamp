from django.contrib import admin
from django.urls import reverse
from .models import Project, Task, Comment


class ProjectAdmin(admin.ModelAdmin):
    readonly_fields = ['id']
    fields = ['id', 'title', 'description', 'due_date', 'is_closed']
    list_display = ['id', 'title', 'description', 'due_date', 'is_closed']
    search_fields = ['title', 'description']
    list_filter = ['due_date', 'is_closed']

    def get_view_on_site_url(self, obj=None):
        return reverse('project-detail', args=(obj.id,)) if obj else None


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    readonly_fields = ['id', 'created']
    fields = ['id', 'created', 'task', 'description']
    raw_id_fields = ['task']


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

    inlines = [CommentInline]

    def get_queryset(self, request):
        return super(TaskAdmin, self).get_queryset(request)\
            .select_related('author', 'assignee')\
            .select_related('project')

    def get_view_on_site_url(self, obj=None):
        return reverse('projects-task-detail', args=(obj.id,)) if obj else None


class CommentAdmin(admin.ModelAdmin):
    list_select_related = True
    readonly_fields = ['id', 'created']
    fields = ['id', 'created', 'task', 'description']
    raw_id_fields = ['task']
    search_fields = ['description']
    list_display = ['id', 'task', 'created', 'description']

    def get_view_on_site_url(self, obj=None):
        return reverse('projects-task-detail', args=(obj.task.id,)) if obj else None


admin.site.register(Project, ProjectAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Comment, CommentAdmin)
