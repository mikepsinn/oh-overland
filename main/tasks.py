import requests
from openhumans.models import OpenHumansMember
from celery import shared_task
import io
import pandas
from .helpers import generate_csv


@shared_task(bind=True)
def foobar(self):
    print('Request: {0!r}'.format(self.request))


@shared_task
def process_batch(fname, oh_id):
    print('task processing {}'.format(oh_id))
    oh_member = OpenHumansMember.objects.get(oh_id=oh_id)
    batch = get_batch(oh_member, fname)
    if type(batch) == dict:
        print('batch is dict')
        f_date = get_date(batch)
        joined_fname = 'overland-data-{}.csv'.format(f_date)
        data, old_file_id = get_existing_data(oh_member, joined_fname)
        print('got data for {}'.format(oh_id))
        if 'locations' in batch.keys():
            print('generate new CSV data')
            new_data = generate_csv(batch)
            if type(data) == pandas.core.frame.DataFrame:
                new_data = pandas.concat(
                    [data, new_data]).reset_index(drop=True)
            str_io = io.StringIO()
            new_data.to_csv(str_io, index=False, encoding='utf-8')
            str_io.flush()
            str_io.seek(0)
            oh_member.upload(
                stream=str_io, filename=joined_fname,
                metadata={
                    'description': 'Summed Overland GPS data',
                    'tags': ['GPS', 'location', 'CSV', 'processed']})
            oh_member.delete_single_file(file_basename=fname)
            if old_file_id:
                oh_member.delete_single_file(file_id=old_file_id)
        else:
            print('batch is not locations')
            oh_member.delete_single_file(file_id=old_file_id)
    else:
        print('batch is not dict')
        oh_member.delete_single_file(file_basename=fname)


def get_batch(oh_member, fname):
    for f in oh_member.list_files():
        if f['basename'] == fname:
            try:
                data = requests.get(f['download_url']).json()
                return data
            except:
                oh_member.delete_single_file(f['id'])
                return []


def get_existing_data(oh_member, fname):
    for f in oh_member.list_files():
        if f['basename'] == fname:
            print('task processing file:')
            print(f)
            data = requests.get(f['download_url']).content
            print('got data')
            data = pandas.read_csv(io.StringIO(
                data.decode('utf-8', errors='ignore')))
            print('read CSV')
            return data, f['id']
    return None, ''


def get_date(batch):
    location = batch['locations'][0]  # get first location entry
    timestamp = location['properties']['timestamp'][:7]  # extract year-month
    return timestamp
