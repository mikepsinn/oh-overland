from django.core.management.base import BaseCommand
from openhumans.models import OpenHumansMember
from celery import current_app


class Command(BaseCommand):
    help = 'Process so far unprocessed data sets'

    def handle(self, *args, **options):
        print(current_app.control.inspect().active_queues())
        oh_members = OpenHumansMember.objects.all()
        for oh_member in oh_members:
            file_number = len(oh_member.list_files())
            print("{}: {}".format(oh_member.oh_id, file_number))
