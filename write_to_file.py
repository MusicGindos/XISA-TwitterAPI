import json


def write_to_file(file_name, data):
    logfile = open(file_name, 'w')
    logfile.write(json.dumps(data))
    logfile.close()
