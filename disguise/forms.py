from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

class DisguiseForm(forms.Form):
    """
    Disguise form
    """
    username = forms.CharField(label=_('User name'),
        required = False)
    user_id = forms.IntegerField(label=_('User ID'),
        required = False)
    update_last_login = forms.BooleanField(label=_('Update last login'),
        required = False)

    def clean_username(self):
        """
        Cleans username field
        """
        username = self.cleaned_data.get('username')
        if not username:
            return None

        qset = User.objects.filter(username=username)

        if len(qset) == 1:
            return qset[0]
        raise forms.ValidationError, _('No such username')

    def clean_user_id(self):
        """
        Cleans 'user_id' field
        """
        user_id = self.cleaned_data.get('user_id')

        if not user_id:
            return None
        qset = User.objects.filter(pk=user_id)

        if len(qset) == 1:
            return qset[0]
        raise forms.ValidationError, _('No such user id')

    def clean(self):
        """
        Clears whole form totally
        """
        if not getattr(self, 'cleaned_data'):
            raise forms.ValidationError, _('No such username or user id')
        return self.cleaned_data

    def get_user(self):
        """
        Returns selected user object
        """
        assert self.is_valid()

        for field in ['username', 'user_id']:
            user = self.cleaned_data.get(field)

            if not isinstance(user, User):
                continue
            return user
        raise ValueError, 'Cannot retrieve user'
