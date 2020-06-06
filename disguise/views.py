from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect
from django.views import generic

from .forms import get_disguise_form_class
from .utils import can_disguise, swap_user

User = get_user_model()


class DisguiseMixin(UserPassesTestMixin):
    """
    A mixin class adding some handy tools to disguise view classes
    """
    raise_exception = True

    def test_func(self):
        return can_disguise(self.request)

    def get_http_referer(self):
        return self.request.META.get('HTTP_REFERER', '/')

    def get_success_url(self):
        return self.get_http_referer()

    def on_success(self):
        return redirect(self.get_success_url())


class Mask(DisguiseMixin, generic.FormView):
    template_name = 'disguise/form.html'

    def get_form_class(self):
        return get_disguise_form_class()

    def form_valid(self, form):
        swap_user(request=self.request,
                  old_user=self.request.user,
                  new_user=form.get_user())
        return self.on_success()


class Unmask(DisguiseMixin, generic.View):
    def get(self, request, *args, **kwargs):
        if hasattr(request, 'original_user'):
            swap_user(request=request,
                      old_user=request.user,
                      new_user=request.original_user)
        return self.on_success()


class MaskById(DisguiseMixin, generic.DetailView):
    queryset = User.objects.all()

    def get(self, request, *args, **kwargs):
        swap_user(request,
                  old_user=self.request.user,
                  new_user=self.get_object())
        return self.on_success()
