from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Users'

    '''imports signals from signals.py'''
    def ready(self):
        import Users.signals
