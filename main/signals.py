from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver

from .models import OverlandUser


@receiver(user_logged_in)
def create_overland_user(sender, request, user, **kwargs):
    OverlandUser.objects.get_or_create(oh_member=user.openhumansmember)
