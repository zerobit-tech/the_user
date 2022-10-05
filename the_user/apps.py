from django.apps import AppConfig


class TheUserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'the_user'

    def ready(self):
        # import the_users.signals
        from . import signals
        try:
            from .initial_load import create_initial_user_groups,create_initial_permissions, create_service_user
            create_service_user()
            create_initial_user_groups()
            create_initial_permissions()
        except Exception as e:
            pass