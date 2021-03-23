from django.contrib import admin
from django.contrib.auth.models import Permission, ContentType
from django.contrib.admin.models import LogEntry


class ContentTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'app_label', 'model']
    list_filter = ['app_label']
    search_fields = ['app_label', 'model']
    readonly_fields = ['id']
    fields = ['id', 'app_label', 'model']


class LogEntryAdmin(admin.ModelAdmin):
    list_display = ['id', 'action_time', 'user', 'content_type', 'action_flag', 'object_repr']
    list_filter = ['user', 'content_type', 'action_flag']
    readonly_fields = ['id', 'action_time']
    fields = [
        'id', 'action_time', 'user', 'content_type',
        'action_flag', 'object_id', 'object_repr', 'change_message'
    ]
    raw_id_fields = ['content_type', 'user']


class PermissionsAdmin(admin.ModelAdmin):
    list_select_related = True
    list_display = ['id', 'name', 'content_type', 'codename']
    list_filter = ['content_type']
    raw_id_fields = ['content_type']


admin.site.register(ContentType, ContentTypeAdmin)
admin.site.register(LogEntry, LogEntryAdmin)
admin.site.register(Permission, PermissionsAdmin)

