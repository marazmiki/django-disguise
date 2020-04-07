from django import apps


class ExampleProjectApp(apps.AppConfig):
    name = 'example_project'

    def ready(self):
        from django.contrib.auth import get_user_model
        from disguise.signals import disguise_applied, disguise_removed
        from . import signal_handlers

        disguise_applied.connect(
            receiver=signal_handlers.on_disguise_applied,
            sender=get_user_model(),
            dispatch_uid='example_project.apps'
        )
        disguise_removed.connect(
            receiver=signal_handlers.on_disguise_removed,
            sender=get_user_model(),
            dispatch_uid='example_project.apps'
        )
