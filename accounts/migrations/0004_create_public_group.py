
from django.db import migrations
from django.contrib.auth.management import create_permissions


def create_public_group(apps, schema_editor):
    """Make public group after auth migrations.

    """
    for app_config in apps.get_app_configs():
        app_config.models_module = True
        create_permissions(app_config, apps=apps, verbosity=1)
        app_config.models_module = None

    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')
    User = apps.get_model('accounts', 'User')
    group_public, _ = Group.objects.get_or_create(name='public')
    perms = Permission.objects.all()
    perms_public = perms.exclude(content_type__app_label__in=['auth', 'admin', 'sessions', 'contenttypes'])\
        .filter(codename__startswith='view_')
    group_public.permissions.set(perms_public)
    group_public.permissions.add(Permission.objects.get(
        content_type__app_label='projects',
        codename='add_comment')
    )

    group_public.user_set.set(User.objects.all())


def delete_public_group(apps, schema_editor):
    """Delete public group in migrations rollback.

    """
    Group = apps.get_model('auth', 'Group')
    try:
        group_public = Group.objects.get(name='public')
        group_public.delete()
    except group_public.DoesNotExist:
        pass


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('projects', '0010_project_documents'),
        ('contenttypes', '0002_remove_content_type_name'),
        ('accounts', '0003_user_birthdate'),
    ]

    operations = [
        migrations.RunPython(create_public_group, delete_public_group)
    ]
