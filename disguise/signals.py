from django.core.signals import Signal

disguise_applied = Signal(providing_args=['original_user', 'old_user',
                                          'new_user', 'request'])
disguise_removed = Signal(providing_args=['original_user',
                                          'disguised_in_user', 'request'])
