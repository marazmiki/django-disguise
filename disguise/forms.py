from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from . import conf

User = get_user_model()


class DisguiseFormBase(forms.Form):
    def get_user(self):
        """
        Returns a selected user instance
        """
        raise NotImplementedError()


class DisguiseForm(DisguiseFormBase):
    username = forms.CharField(label=_('User name'), required=False)
    user_id = forms.IntegerField(label=_('User ID'), required=False)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not username:
            return None
        qset = User.objects.filter(username=username)
        if qset.exists():
            return qset.get()
        raise forms.ValidationError(_('No such username'))

    def clean_user_id(self):
        user_id = self.cleaned_data.get('user_id')
        if not user_id:
            return None
        qset = User.objects.filter(pk=user_id)
        if qset.exists():
            return qset.get()
        raise forms.ValidationError(_('No such user id'))

    def clean(self):
        """
        Clears whole form totally
        """
        if not any((
                self.cleaned_data.get('user_id'),
                self.cleaned_data.get('username')
        )):
            raise forms.ValidationError(
                _('Please enter either username or user id')
            )
        return self.cleaned_data

    def get_user(self):
        """
        Returns a selected user instance
        """
        if not self.is_valid():
            raise RuntimeError(
                'The `get_user() method should be called only '
                'the form is valid'
            )
        return next((v for k, v in self.cleaned_data.items() if v), None)


def get_disguise_form_class():
    if not conf.CUSTOMIZED_WIDGET_FORM_CLASS:
        return DisguiseForm
    return conf.CUSTOMIZED_WIDGET_FORM_CLASS
