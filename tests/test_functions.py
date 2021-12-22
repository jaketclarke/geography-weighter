from guts.weighter import *
from guts.functions import get_filename_from_path
from guts.functions import get_filename_from_path_without_extension
from guts.functions import empty_directory
import pytest
import os
from pathlib import Path

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

def test_get_filename_from_path_without_extension_works():
    
    s = 'dir1/test.csv'
    assert get_filename_from_path_without_extension(s) == 'test'

def test_get_filename_from_path_without_extension_nofilepath_two():
    
    s = 'test.xlsx'
    assert get_filename_from_path_without_extension(s) == 'test'

def test_get_filename_from_path_without_extension_manypaths():
    
    s = 'dir1/dir2/dir3/test.csv'
    assert get_filename_from_path_without_extension(s) == 'test'

def test_empty_directory_works():
    folder = 'output'
    # ensure something in output dir
    Path(f'{folder}{os.sep}fake.txt').touch()
    # # delete dir
    empty_directory(folder)
    # # assert empty
    assert len(os.listdir(folder)) == 0
