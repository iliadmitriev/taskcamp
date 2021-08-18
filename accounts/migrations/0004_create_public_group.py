
from django.db import migrations
from django.contrib.auth.management import create_permissions


def create_public_group(apps, schema_editor):
    """Make public group after auth migrations.

    """
    for app_config in apps.get_app_configs():
        app_config.models_module = True
        create_permissions(app_config, interactive=False, using=schema_editor.connection.alias, apps=apps, verbosity=1)
        app_config.models_module = None

    groups = apps.get_model('auth', 'Group').objects.using(schema_editor.connection.alias)
    permissions = apps.get_model('auth', 'Permission').objects.using(schema_editor.connection.alias)
    users = apps.get_model('accounts', 'User').objects.using(schema_editor.connection.alias)
    group_public, _ = groups.get_or_create(name='public')
    perms = permissions.all()
    perms_public = perms.exclude(content_type__app_label__in=['auth', 'admin', 'sessions', 'contenttypes'])\
        .filter(codename__startswith='view_')
    group_public.permissions.set(perms_public)
    group_public.permissions.add(permissions.get(
        content_type__app_label='projects',
        codename='add_comment')
    )

    group_public.user_set.set(users.all())


def delete_public_group(apps, schema_editor):
    """Delete public group in migrations rollback.

    """
    Group = apps.get_model('auth', 'Group')
    try:
        group_public = Group.objects.using(schema_editor.connection.alias).get(name='public')
        group_public.delete()
    except group_public.DoesNotExist:
        pass


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '__latest__'),
        ('contenttypes', '__latest__'),
        ('projects', '__latest__'),
        ('accounts', '0003_user_birthdate'),
    ]

    operations = [
        migrations.RunPython(create_public_group, delete_public_group)
    ]
