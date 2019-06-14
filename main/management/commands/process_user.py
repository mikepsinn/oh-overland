from django.core.management.base import BaseCommand
from openhumans.models import OpenHumansMember
from main.tasks import process_batch


class Command(BaseCommand):
    help = 'Process so far unprocessed data sets'

    def add_arguments(self, parser):
        parser.add_argument(
            "-u, --user",
            dest="oh_id",
            required=True,
            help="the open humans ID to queue",
            )

    def handle(self, *args, **options):
        oh_member = OpenHumansMember.objects.get(oh_id=options["oh_id"])
        files = oh_member.list_files()
        batches = []
        for f in files:
            if f['basename'].startswith('overland-batch-'):
                batches.append(f['basename'])
        batches.sort()
        for f in batches:
            process_batch.delay(f, oh_member.oh_id)
