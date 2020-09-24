from django.core.management.base import BaseCommand
from openhumans.models import OpenHumansMember
import pandas
from collections import defaultdict
import io
import requests


class Command(BaseCommand):
    help = 'Process so far unprocessed data sets'

    def handle(self, *args, **options):
        oh_members = OpenHumansMember.objects.all()
        for oh_member in oh_members:
            print('working on member {}'.format(oh_member.oh_id))
            overland_files = defaultdict(list)
            try:
                for f in oh_member.list_files():
                    if f['basename'].startswith('overland-data') and f['basename'].endswith('.csv'):
                        overland_files[f['basename']].append(f)
                for k, v in overland_files.items():
                    if len(v) > 1:
                        data_frames = []
                        for entry in v:
                            data = requests.get(entry['download_url']).content
                            data = pandas.read_csv(io.StringIO(
                                data.decode('utf-8', errors='ignore')))
                            data_frames.append(data)
                        merged_df = data_frames[0]
                        for df in data_frames[1:]:
                            merged_df = pandas.concat([merged_df, df])
                        merged_df = merged_df.drop_duplicates(keep='first')
                        merged_df = merged_df.sort_values('timestamp', ascending=True)
                        str_io = io.StringIO()
                        merged_df.to_csv(str_io, index=False, encoding='utf-8')
                        str_io.flush()
                        str_io.seek(0)
                        oh_member.upload(
                            stream=str_io, filename=k,
                            metadata={
                                'description': 'Summed Overland GPS data',
                                'tags': ['GPS', 'location', 'CSV', 'processed']})
                        for entry in v:
                            oh_member.delete_single_file(file_id=entry['id'])
            except:
                pass
