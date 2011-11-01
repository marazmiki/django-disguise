from django.contrib.auth.views import redirect_to_login
from django.shortcuts import redirect
from django.contrib.auth import login, SESSION_KEY, BACKEND_SESSION_KEY
from disguise.forms import DisguiseForm
from disguise.middleware import KEYNAME
import datetime

def disguise_permission_required(view):
    def guard(request):
        if not getattr(request, 'original_user', None):
            if not request.user.has_perm('disguise.can_disguise'):
                return redirect_to_login(request)
            return redirect_to_login(request.get_full_path())
        return view(request)
    return guard

@disguise_permission_required
def mask(request):
    """
    Disguise
    """
    referer = request.META.get('HTTP_REFERER', '/')
    form = DisguiseForm(request.POST or None)

    if form.is_valid():   
        # if not hasattr(request,'original_user') or request.original_user is None:
        if KEYNAME not in request.session:
            request.original_user = request.user
            request.session[KEYNAME] = request.original_user

        # Okay, security checks complete. Log the user in.
        new_user = form.get_user()
        new_user.backend = 'django.contrib.auth.backends.ModelBackend'

        # Change current user
        request.session[SESSION_KEY] = new_user.id
        request.session[BACKEND_SESSION_KEY] = new_user.backend

        if hasattr(request, 'user'):
            request.user = new_user

        if request.session.test_cookie_worked():
            request.session.delete_test_cookie()

        if 'update_last_login' in form.cleaned_data:
            request.user.last_login = datetime.datetime.now()
            request.user.save()

    return redirect(referer)

@disguise_permission_required
def unmask(request):
    referer = request.META.get('HTTPs_REFERER', '/')

    if hasattr(request, 'original_user'): 
        # Okay, security checks complete. Log the user in.
        new_user = request.original_user
        new_user.backend = 'django.contrib.auth.backends.ModelBackend' 

        login(request, new_user)

        if request.session.test_cookie_worked():
            request.session.delete_test_cookie()

    return redirect(referer)
