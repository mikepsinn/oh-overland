import requests
from openhumans.models import OpenHumansMember
from celery import shared_task
import io
import json


@shared_task(bind=True)
def foobar(self):
    print('Request: {0!r}'.format(self.request))


@shared_task
def process_batch(fname, oh_id):
    oh_member = OpenHumansMember.objects.get(oh_id=oh_id)
    data, old_file_id = get_existing_data(oh_member, 'overland-data.json')
    batch, _ = get_existing_data(oh_member, fname)
    if 'locations' in batch.keys():
        data += batch['locations']
        str_io = io.StringIO()
        json.dump(data, str_io)
        str_io.flush()
        str_io.seek(0)
        oh_member.upload(
            stream=str_io, filename='overland-data.json',
            metadata={
                'description': 'Summed Overland GPS data',
                'tags': ['GPS', 'location', 'json', 'processed']})
        oh_member.delete_single_file(file_basename=fname)
        if old_file_id:
            oh_member.delete_single_file(file_id=old_file_id)


def get_existing_data(oh_member, fname):
    for f in oh_member.list_files():
        if f['basename'] == fname:
            data = requests.get(f['download_url']).json()
            return data, f['id']
    return [], ''
