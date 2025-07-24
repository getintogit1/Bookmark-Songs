from django.apps import AppConfig


class SongsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'songs'

    def ready(self):
        # import signal handlers
        import songs.signals
"""You import the signals for this application in the ready() method so that they are imported when the
songs application is loaded.
"""
