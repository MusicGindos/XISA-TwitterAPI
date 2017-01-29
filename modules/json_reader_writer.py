from datetime import *
import json

fmt = '%Y-%m-%d %H:%M:%S'


def calculate_differences_between_datetime(old_time):  # pass argument as "2017-01-16 17:41:08" format
    old = datetime.strptime(old_time, fmt)
    now = datetime.strptime(str(datetime.now()).split('.')[0], fmt)
    dif = ((now-old).total_seconds())/60
    return dif


def update_time_by_key(key, inner_key=None):  # update time in times.json
    value = str(datetime.strptime(str(datetime.now()).split('.')[0], fmt))
    with open('data/times.json', 'r') as file:
        json_data = json.load(file)
        if inner_key is None:
            json_data[key] = value
        else:
            json_data[key][inner_key] = value
    with open('data/times.json', 'w') as file:
        file.write(json.dumps(json_data))


def read_from_times_json(key):  # read time from times.json
    with open('data/times.json') as data_file:
        data = json.load(data_file)
        return data[key]


def read_from_times_with_categories(key, category):  # read times of category for celebs
    with open('data/times.json') as data_file:
        data = json.load(data_file)
        return data[key][category]


def write_to_data_json(key, value, category=None):  # write data by key
    with open('data/data.json', 'r') as file:
        json_data = json.load(file)
        if category is None:
            json_data[key] = value
        else:
            json_data[key][category] = value
    with open('data/data.json', 'w') as file:
        file.write(json.dumps(json_data))


def read_from_data_json(key, category=None):  # read data from json by key and category as option
    with open('data/data.json') as data_file:
        data = json.load(data_file)
        if category is None:
            return data[key]
        else:
            return data[key][category]


def is_category(category_to_check):  # check if category is exist
    categories = read_from_data_json("categories_only")
    for category in categories:
        if category == category_to_check:
            return True
    return False
