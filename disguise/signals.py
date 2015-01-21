# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from django.core.signals import Signal

disguise_applied = Signal(providing_args=['original_user', 'new_user'])
disguise_disapplied = Signal(providing_args=['original_user', 'old_user'])
