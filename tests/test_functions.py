from guts.weighter import *
from guts.functions import get_filename_from_path
from guts.functions import get_filename_from_path_without_extension
from guts.functions import empty_directory
from guts.functions import make_directorytree_if_not_exists
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
    """
    Test function to empty directory
    """
    folder = 'output'
    # ensure something in output dir
    Path(f'{folder}{os.sep}fake.txt').touch()
    # # delete dir
    empty_directory(folder)
    # # assert empty
    assert len(os.listdir(folder)) == 0

def test_empty_directory_nested_works():
    """
    Test function to empty directory with nested files
    """
    folder = 'output'
    # ensure something in output dir
    Path(f'{folder}{os.sep}fake.txt').touch()
    make_directorytree_if_not_exists(f'{folder}{os.sep}{folder}')
    Path(f'{folder}{os.sep}{folder}{os.sep}fake.txt').touch()
    # # delete dir
    empty_directory(folder)
    # # assert empty
    assert len(os.listdir(folder)) == 0

def test_make_directorytree_if_not_exists_works():
    """
    Test to ensure creating a directory works
    """
    folder = 'output'
    subfolder = 'thisisatest'
    path = f'{folder}{os.sep}{subfolder}'
    #ensure empty
    if os.path.isdir(path):
        empty_directory(path)
    #create
    make_directorytree_if_not_exists(path)
    #assert exists
    assert os.path.isdir(path)