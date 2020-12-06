import json
import os
from termcolor import colored
import six
from pyfiglet import figlet_format


def load_json(file):
    with open(file) as file:
        return json.load(file)


def dump_json(data, outfilepath):
    with open(outfilepath, 'w') as outfile:
        json.dump(data, outfile)


def make_directorytree_if_not_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)


def log(string, color, font="slant", figlet=False):
    if colored:
        if not figlet:
            six.print_(colored(string, color))
        else:
            six.print_(colored(figlet_format(
                string, font=font), color))
    else:
        six.print_(string)
