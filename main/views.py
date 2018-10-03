from django.conf import settings
from django.contrib import messages
from django.contrib.auth import logout
from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import redirect, render
from django.utils.safestring import mark_safe

from openhumans.models import OpenHumansMember


def index(request):
    """
    Starting page for app.
    """
    try:
        auth_url = OpenHumansMember.get_auth_url()
    except ImproperlyConfigured:
        auth_url = None
    if not auth_url:
        messages.info(request,
                      mark_safe(
                          '<b>You need to set up your ".env"'
                          ' file!</b>'))

    context = {'auth_url': auth_url}
    return render(request, 'main/index.html', context=context)


def logout_user(request):
    """
    Logout user
    """
    if request.method == 'POST':
        logout(request)
    redirect_url = settings.LOGOUT_REDIRECT_URL
    return redirect(redirect_url)
