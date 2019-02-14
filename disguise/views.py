from django.contrib.auth.views import redirect_to_login
from django.contrib.auth import login
from django.shortcuts import redirect
from django.views.generic import View, FormView
from disguise.forms import DisguiseForm
from disguise.const import KEYNAME, SESSION_KEY, BACKEND_SESSION_KEY, BACKEND
from disguise.utils import can_disguise
from disguise.signals import disguise_applied, disguise_disapplied


class DisguiseMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if not can_disguise(request):
            return redirect_to_login(request)
        return super(DisguiseMixin, self).dispatch(request, *args, **kwargs)

    def get_http_referer(self):
        return self.request.META.get('HTTP_REFERER', '/')

    def test_cookie(self):
        if self.request.session.test_cookie_worked():
            self.request.session.delete_test_cookie()


def swap_user(request, old_user, new_user):
    if KEYNAME not in request.session:
        request.original_user = old_user
        request.session[KEYNAME] = request.original_user.pk

    new_user.backend = BACKEND

    request.session[SESSION_KEY] = new_user.id
    request.session[BACKEND_SESSION_KEY] = new_user.backend

    login(request, new_user)

    if request.session.test_cookie_worked():
        request.session.delete_test_cookie()
    if KEYNAME not in request.session:
        request.original_user = request.user
        request.session[KEYNAME] = request.original_user.pk



class MaskView(DisguiseMixin, FormView):
    form_class = DisguiseForm

    def form_valid(self, form):
        old_user = self.request.user
        new_user = form.get_user()
        swap_user(request=self.request,
                  old_user=old_user,
                  new_user=new_user)
        disguise_applied.send(sender=new_user.__class__,
                              original_user=old_user,
                              new_user=new_user)
        return redirect(self.get_http_referer())


class UnmaskView(DisguiseMixin, View):
    def get(self, request, *args, **kwargs):
        if hasattr(request, 'original_user'):
            # Okay, security checks complete. Log the user in.
            old_user = request.user
            new_user = request.original_user
            new_user.backend = BACKEND

            login(request, new_user)

            disguise_disapplied.send(sender=new_user.__class__,
                                     original_user=request.original_user,
                                     old_user=old_user)
        self.test_cookie()
        return redirect(self.get_http_referer())
