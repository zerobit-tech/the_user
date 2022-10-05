from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from .initial_groups import ( GROUPS,  GROUP_PERMISSIONS)

import logging
logger = logging.getLogger('ilogger')







def create_service_user():
        user = User.objects.get_or_create(username = 'SYSTEM',
                                 first_name = "",
                                 last_name = "",
                                 email="system@example.com",
                                 password="e<7w'WH@_b",
                                 is_active = False
                                 )


def create_initial_user_groups():
        for group in GROUPS:
            new_group, created = Group.objects.get_or_create(name=group)
            if created:
                pass



def create_initial_permissions():

    group_content_type = ContentType.objects.get(app_label='auth', model='group')

    for group_name in GROUP_PERMISSIONS.keys():
        group, _ = Group.objects.get_or_create(name=group_name)
        admin_group, _ = Group.objects.get_or_create(name="Admin")

        group_permission = GROUP_PERMISSIONS[group_name]

        for name, code_name in group_permission:
            permission, created = Permission.objects.get_or_create(name=name, codename=code_name,content_type=group_content_type)
            if created:
                pass
            group.permissions.add(permission)
            admin_group.permissions.add(permission)