import pandas
from collections import defaultdict


def generate_csv(overland_json):
    '''
    generate CSV from overland batch
    '''
    flat_data_dict = defaultdict(list)
    for entry in overland_json['locations']:
        if 'motion' in entry['properties'].keys():
            flat_data_dict = convert_location_entry(flat_data_dict, entry)
    df = pandas.DataFrame(data=flat_data_dict)
    return df


def convert_location_entry(flat_data_dict, entry):
    flat_data_dict['longitude'].append(entry['geometry']['coordinates'][0])
    flat_data_dict['latitude'].append(entry['geometry']['coordinates'][1])
    if 'activity' in entry['properties'].keys():
        flat_data_dict['activity'].append(entry['properties']['activity'])
    else:
        flat_data_dict['activity'].append('')
    flat_data_dict['altitude'].append(entry['properties']['altitude'])
    flat_data_dict['battery_level'].append(
        entry['properties']['battery_level'])
    flat_data_dict['battery_state'].append(
        entry['properties']['battery_state'])
    if 'deferred' in entry['properties'].keys():
        flat_data_dict['deferred'].append(entry['properties']['deferred'])
    else:
        flat_data_dict['deferred'].append('')
    if 'desired_accuracy' in entry['properties'].keys():
        flat_data_dict['desired_accuracy'].append(
            entry['properties']['desired_accuracy'])
    else:
        flat_data_dict['desired_accuracy'].append('')
    flat_data_dict['horizontal_accuracy'].append(
        entry['properties']['horizontal_accuracy'])
    flat_data_dict['motion'].append('\t'.join(entry['properties']['motion']))
    if 'pauses' in entry['properties'].keys():
        flat_data_dict['pauses'].append(entry['properties']['pauses'])
    else:
        flat_data_dict['pauses'].append('')
    if 'significant_change' in entry['properties'].keys():
        flat_data_dict['significant_change'].append(
            entry['properties']['significant_change'])
    else:
        flat_data_dict['significant_change'].append('')
    flat_data_dict['speed'].append(entry['properties']['speed'])
    flat_data_dict['timestamp'].append(entry['properties']['timestamp'])
    flat_data_dict['vertical_accuracy'].append(
        entry['properties']['vertical_accuracy'])
    flat_data_dict['wifi'].append(entry['properties']['wifi'])
    return flat_data_dict
