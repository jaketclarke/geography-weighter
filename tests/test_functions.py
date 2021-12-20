from guts.weighter import *
from guts.functions import *
import pytest
import os

def test_get_filename_from_path_nofilepath():

    s = 'test.csv'
    assert get_filename_from_path(s) == s

def test_get_filename_from_path_works():
    
    s = 'dir1/test.csv'
    assert get_filename_from_path(s) == 'test.csv'


def test_get_filename_from_path_nofilepath_two():
    
    s = 'test.xlsx'
    assert get_filename_from_path(s) == s

def test_get_filename_from_path_manypaths():
    
    s = 'dir1/dir2/dir3/test.csv'
    assert get_filename_from_path(s) == 'test.csv'