import random
import string
from django.db import models

from openhumans.models import OpenHumansMember

ENDPOINT_TOKEN_LEN = 10


def generate_endpoint_token(len=ENDPOINT_TOKEN_LEN):
    return ''.join(random.choices(string.ascii_lowercase +
                                  string.digits, k=len))


class OverlandUser(models.Model):
    oh_member = models.OneToOneField(OpenHumansMember,
                                     on_delete=models.CASCADE)
    endpoint_token = models.CharField(max_length=ENDPOINT_TOKEN_LEN,
                                      unique=True,
                                      default=generate_endpoint_token)
