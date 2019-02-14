from django.contrib.auth import get_user_model
from django.contrib.auth.views import redirect_to_login
from django.shortcuts import redirect
from django.views.generic import FormView, View

from disguise.forms import DisguiseForm
from disguise.signals import disguise_applied, disguise_disapplied
from disguise.utils import can_disguise, swap_user

User = get_user_model()


class DisguiseMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if not can_disguise(request):
            return redirect_to_login(request)
        return super(DisguiseMixin, self).dispatch(request, *args, **kwargs)

    def get_http_referer(self):
        return self.request.META.get('HTTP_REFERER', '/')


class MaskView(DisguiseMixin, FormView):
    form_class = DisguiseForm

    def form_valid(self, form):
        old_user = self.request.user
        new_user = form.get_user()

        swap_user(request=self.request,
                  old_user=old_user,
                  new_user=new_user)

        disguise_applied.send(sender=User,
                              original_user=old_user,
                              new_user=new_user)

        return redirect(self.get_http_referer())


class UnmaskView(DisguiseMixin, View):
    def get(self, request, *args, **kwargs):
        if hasattr(request, 'original_user'):
            old_user = request.user
            new_user = request.original_user

            swap_user(request=request,
                      old_user=old_user,
                      new_user=new_user)

            disguise_disapplied.send(sender=User,
                                     original_user=new_user,
                                     old_user=old_user)
        return redirect(self.get_http_referer())
