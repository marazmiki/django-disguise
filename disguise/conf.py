from django import conf
from django.utils.module_loading import import_string

__all__ = ['CUSTOMIZED_CAN_DISGUISE', 'CUSTOMIZED_WIDGET_FORM_CLASS']

settings = getattr(conf.settings, 'DISGUISE', {})


try:
    CUSTOMIZED_WIDGET_FORM_CLASS = import_string(settings['widget_form'])
except (ImportError, KeyError):
    CUSTOMIZED_WIDGET_FORM_CLASS = None


# Customized "can_disguise" function support
try:
    # Here, we would not check if the function is callable as
    # we delegated this one to the django's checks framework.
    CUSTOMIZED_CAN_DISGUISE = import_string(settings['can_disguise'])
except (ImportError, KeyError):
    CUSTOMIZED_CAN_DISGUISE = None
