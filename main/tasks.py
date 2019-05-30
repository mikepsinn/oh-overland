import requests
from openhumans.models import OpenHumansMember
from celery import shared_task
import io
import datetime
import pandas
from .helpers import generate_csv


@shared_task(bind=True)
def foobar(self):
    print('Request: {0!r}'.format(self.request))


@shared_task
def process_batch(fname, oh_id):
    oh_member = OpenHumansMember.objects.get(oh_id=oh_id)
    batch = get_batch(oh_member, fname)
    print('got batch')
    f_date = get_date(fname)
    joined_fname = 'overland-data-{}.csv'.format(f_date)
    print('getting exsiting data')
    data, old_file_id = get_existing_data(oh_member, joined_fname)
    print('got exsiting data')
    print('batch:')
    print(batch)
    if type(batch) == dict:
        if 'locations' in batch.keys():
            print('generate new CSV data')
            new_data = generate_csv(batch)
            if data:
                new_data = pandas.concat(
                    [data, new_data]).reset_index(drop=True)
            str_io = io.StringIO()
            new_data.to_csv(str_io, index=False)
            str_io.flush()
            str_io.seek(0)
            oh_member.upload(
                stream=str_io, filename=joined_fname,
                metadata={
                    'description': 'Summed Overland GPS data',
                    'tags': ['GPS', 'location', 'json', 'processed']})
            oh_member.delete_single_file(file_basename=fname)
            if old_file_id:
                oh_member.delete_single_file(file_id=old_file_id)
    else:
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
            data = requests.get(f['download_url']).content
            data = pandas.read_csv(io.StringIO(data.decode('utf-8')))
            return data, f['id']
    return None, ''


def get_date(fname):
    tstamp = int(float(fname.replace(
                        '.json',
                        '').replace(
                            'overland-batch-',
                            '')))
    tstamp = datetime.datetime.fromtimestamp(tstamp)
    return tstamp.strftime('%Y-%m')
