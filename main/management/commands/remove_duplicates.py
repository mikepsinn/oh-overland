from django.core.management.base import BaseCommand
from openhumans.models import OpenHumansMember


class Command(BaseCommand):
    help = 'Process so far unprocessed data sets'

    def handle(self, *args, **options):
        oh_members = OpenHumansMember.objects.all()
        for oh_member in oh_members:
