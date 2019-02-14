from django import forms
from django.utils.translation import ugettext_lazy as _

from disguise.compat import get_user_model


User = get_user_model()


class DisguiseForm(forms.Form):
    """
    Disguise form
    """
    username = forms.CharField(label=_('User name'), required=False)
    user_id = forms.IntegerField(label=_('User ID'), required=False)

    def clean_username(self):
        """
        Cleans username field
        """
        username = self.cleaned_data.get('username')

        if not username:
            return None

        qset = User.objects.filter(username=username)

        if qset.exists():
            return qset.get()
        raise forms.ValidationError(_('No such username'))

    def clean_user_id(self):
        """
        Cleans 'user_id' field
        """
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
        cleaned_data = getattr(self, 'cleaned_data', {})

        if not cleaned_data.get('user_id') and \
                not cleaned_data.get('username'):
            raise forms.ValidationError(
                _('Please enter either username or user id')
            )
        return self.cleaned_data

    def get_user(self):
        """
        Returns a selected user instance
        """
        assert self.is_valid()
        return next((v for k, v in self.cleaned_data.items()), None)
