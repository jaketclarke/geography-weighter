"""
Module of helper functions to be used through the project
"""
import json
import os
from termcolor import colored
import six
from pyfiglet import figlet_format


def load_json(file):
    """[summary]

    Loads a json file and returns data

    Args:
        file ([type]): [description]

    Returns:
        [type]: [description]
    """
    with open(file, encoding='UTF-8') as file:
        return json.load(file)


def dump_json(data, outfilepath):
    """
    Takes a data file and dumps json

    Args:
        data ([type]): [description]
        outfilepath ([type]): [description]
    """
    with open(outfilepath, 'w', encoding='UTF-8') as outfile:
        json.dump(data, outfile)


def make_directorytree_if_not_exists(path):
    """
    Ensure a directory path exists

    Args:
        path ([type]): [description]
    """
    if not os.path.exists(path):
        os.makedirs(path)


def log(string, color, font="slant", figlet=False):
    """Log string to cmd line

    Args:
        string ([type]): [description]
        color ([type]): [description]
        font (str, optional): [description]. Defaults to "slant".
        figlet (bool, optional): [description]. Defaults to False.
    """
    if color:
        if not figlet:
            six.print_(colored(string, color))
        else:
            six.print_(colored(figlet_format(
                string, font=font), color))
    else:
        six.print_(string)


def get_filename_from_path(filepath: str) -> str:
    """
    Strip the filename from a path eg test.sql from foobar/test.sql

    Args:
        filepath (str): [description]

    Returns:
        str: [description]
    """
    filename = ''

    if '/' in filepath:
        filename = filepath[filepath.rindex('/')+1:]
    else:
        filename = filepath

    return filename

def get_filename_from_path_without_extension(filepath: str) -> str:
    """
    Strip the filename and extension from a path eg test from foobar/test.sql

    Args:
        filepath (str): [description]

    Returns:
        str: [description]
    """
    filename = ''

    if '/' in filepath:
        filename = filepath[filepath.rindex('/')+1:]
    else:
        filename = filepath

    if '.' in filename:
        filename = filename[:filename.rindex('.')]

    return filename
