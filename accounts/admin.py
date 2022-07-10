"""
Accounts admin module.
"""
from django.contrib import admin
from django.contrib.admin.models import LogEntry
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import ContentType, Permission
from django.utils.translation import gettext_lazy as _

from .models import User


class UserAccountAdmin(UserAdmin):
    """User Accounts model admin."""

    fieldsets = (
        (None, {"fields": ("id", "email", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "birthdate")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["email", "password1", "password2"],
            },
        ),
    )
    list_display = [
        "id",
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "is_superuser",
    ]
    list_display_links = ["id", "email"]
    list_filter = ["is_active", "is_staff", "is_superuser", "groups__name"]
    search_fields = ["email", "first_name", "last_name"]
    ordering = ["-id"]
    readonly_fields = ["id"]


class ContentTypeAdmin(admin.ModelAdmin):
    """Content types model admin."""

    list_display = ["id", "app_label", "model"]
    list_filter = ["app_label"]
    search_fields = ["app_label", "model"]
    readonly_fields = ["id"]
    fields = ["id", "app_label", "model"]


class PermissionsAdmin(admin.ModelAdmin):
    """Permissions model admin."""

    list_select_related = True
    list_display = ["id", "name", "content_type", "codename"]
    list_filter = ["content_type"]
    raw_id_fields = ["content_type"]


class LogEntryAdmin(admin.ModelAdmin):
    """Logs model admin."""

    list_display = [
        "id",
        "action_time",
        "user",
        "content_type",
        "action_flag",
        "object_repr",
    ]
    list_filter = ["user", "content_type", "action_flag"]
    readonly_fields = ["id", "action_time"]
    fields = [
        "id",
        "action_time",
        "user",
        "content_type",
        "action_flag",
        "object_id",
        "object_repr",
        "change_message",
    ]
    raw_id_fields = ["content_type", "user"]


admin.site.register(User, UserAccountAdmin)
admin.site.register(ContentType, ContentTypeAdmin)
admin.site.register(Permission, PermissionsAdmin)
admin.site.register(LogEntry, LogEntryAdmin)
