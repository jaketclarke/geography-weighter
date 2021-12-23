"""
Tests for the functions in guts.functions
"""
import os
from pathlib import Path

from guts.functions import (
    empty_directory,
    get_filename_from_path,
    get_filename_from_path_without_extension,
    make_directorytree_if_not_exists,
)


def test_get_filename_from_path_nofilepath():
    """
    Test for getting filename from a filepath - no path
    """

    filepath = "test.csv"
    assert get_filename_from_path(filepath) == "test.csv"


def test_get_filename_from_path_works():
    """
    Test for getting filename from a filepath - handle a directory
    """

    filepath = "dir1/test.csv"
    assert get_filename_from_path(filepath) == "test.csv"


def test_get_filename_from_path_nofilepath_two():
    """
    Test for getting filename from a filepath - no path
    """
    filepath = "test.xlsx"
    assert get_filename_from_path(filepath) == "test.xlsx"


def test_get_filename_from_path_manypaths():
    """
    Test for getting filename from a filepath - multiple dirs
    """
    filepath = "dir1/dir2/dir3/test.csv"
    assert get_filename_from_path(filepath) == "test.csv"


def test_get_filename_from_path_without_extension_works():
    """
    Test for getting filename without extension from a filepath - no path, no extension
    """
    filepath = "dir1/test"
    assert get_filename_from_path_without_extension(filepath) == "test"


def test_get_filename_from_path_without_extension_nofilepath_two():
    """
    Test for getting filename without extension from a filepath - no path
    """
    filepath = "test.xlsx"
    assert get_filename_from_path_without_extension(filepath) == "test"


def test_get_filename_from_path_without_extension_manypaths():
    """
    Test for getting filename without extension from a filepath - no path
    """
    filepath = "dir1/dir2/dir3/test.csv"
    assert get_filename_from_path_without_extension(filepath) == "test"


def test_empty_directory_works():
    """
    Test function to empty directory
    """
    folder = "output"
    # ensure something in output dir
    Path(f"{folder}{os.sep}fake.txt").touch()
    # # delete dir
    empty_directory(folder)
    # # assert empty
    assert len(os.listdir(folder)) == 0


def test_empty_directory_nested_works():
    """
    Test function to empty directory with nested files
    """
    folder = "output"
    # ensure something in output dir
    Path(f"{folder}{os.sep}fake.txt").touch()
    make_directorytree_if_not_exists(f"{folder}{os.sep}{folder}")
    Path(f"{folder}{os.sep}{folder}{os.sep}fake.txt").touch()
    # # delete dir
    empty_directory(folder)
    # # assert empty
    assert len(os.listdir(folder)) == 0


def test_make_directorytree_if_not_exists_works():
    """
    Test to ensure creating a directory works
    """
    folder = "output"
    subfolder = "thisisatest"
    path = f"{folder}{os.sep}{subfolder}"
    # ensure empty
    if os.path.isdir(path):
        empty_directory(path)
    # create
    make_directorytree_if_not_exists(path)
    # assert exists
    assert os.path.isdir(path)
