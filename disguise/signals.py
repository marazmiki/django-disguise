from django.core.signals import Signal

disguise_applied = Signal(providing_args=['original_user', 'new_user'])
disguise_disapplied = Signal(providing_args=['original_user', 'old_user'])
