from django import conf
from django.utils.module_loading import import_string

__all__ = ['CUSTOMIZED_CAN_DISGUISE']

settings = getattr(conf.settings, 'DISGUISE', {})


# Customized "can_disguise" function support
try:
    # Here, we would not check if the function is callable as
    # we delegated this one to the django's checks framework.
    CUSTOMIZED_CAN_DISGUISE = import_string(settings['can_disguise'])
except (ImportError, KeyError):
    CUSTOMIZED_CAN_DISGUISE = None
