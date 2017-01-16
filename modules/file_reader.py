from datetime import *
import json

fmt = '%Y-%m-%d %H:%M:%S'


def calculate_differences_between_datetime(old_time):  # pass argument as "2017-01-16 17:41:08"
    old = datetime.strptime(old_time, fmt)
    now = datetime.strptime(str(datetime.now()).split('.')[0], fmt)
    dif = ((now-old).total_seconds())/60
    return dif


def update_time_by_key(key):
    value = str(datetime.strptime(str(datetime.now()).split('.')[0], fmt))
    pair = {key: value}
    with open('data/times.json') as file:
        data = json.load(file)
    data.update(pair)
    with open('data/times.json', 'w') as file:
        json.dump(data, file)


def read_from_times_json(key):
    with open('data/times.json') as data_file:
        data = json.load(data_file)
        return data[key]


def write_to_data_json(key, value):
    pair = {key: value}
    with open('data/data.json') as file:
        data = json.load(file)
    data.update(pair)
    with open('data/data.json', 'w') as file:
        json.dump(data, file)


def read_from_data_json(key):
    with open('data/data.json') as data_file:
        data = json.load(data_file)
        return data[key]
