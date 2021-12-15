from django import __version__
from django.core.signals import Signal

if __version__ < '3.1':
    disguise_applied = Signal(providing_args=['original_user', 'old_user',
                                              'new_user', 'request'])
    disguise_removed = Signal(providing_args=['original_user',
                                              'disguised_in_user', 'request'])
else:
    disguise_applied = Signal()
    disguise_removed = Signal()
