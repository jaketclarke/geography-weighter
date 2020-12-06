import json
import os

def load_json(file):
    with open(file) as file:
        return json.load(file)

def dump_json(data, outfilepath):
    with open(outfilepath, 'w') as outfile:
                json.dump(data, outfile)

def make_directorytree_if_not_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)