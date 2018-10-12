import io

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import logout
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils.safestring import mark_safe
from django.views.decorators.csrf import csrf_exempt

from openhumans.models import OpenHumansMember

from .models import OverlandUser


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


@csrf_exempt
def receiver(request, token):
    """
    Endpoint for receiving Overland data
    """
    try:
        oluser = OverlandUser.objects.get(endpoint_token=token)
        print('------------------')
        print('IN RECEIVER FOR {0}'.format(oluser.oh_member.oh_id))
        print(request.method)
        if request.method == 'POST':
            stream = io.BytesIO(request.body)
            metadata = {
                'tags': ['GPS', 'location', 'json'],
                'description': 'Overland GPS data batch'}
            oluser.oh_member.upload(
                stream=stream, filename='overland-data.json',
                metadata=metadata)
            print('FILE CREATED')
        print('------------------')
        return HttpResponse('In receive: OH ID is {0}'.format(
            oluser.oh_member.oh_id))
    except OverlandUser.DoesNotExist:
        return HttpResponse('In receiver: no user')
