from weighter import *
from functions import *
import pytest
import os

# tests for strip_parent_directory
def test_weight_run():
    # create weight class
    w = Weight(input_mode='postcode')
    # load data
    w.get_input_data()
    w.get_weight_data()
    # ensure output dir exists
    make_directorytree_if_not_exists(w.output_dir)
    # process
    w.run_merge_data()
    w.run_process_data()
    w.run_cull_data()
    # export
    w.export_output_data()
    # check export file exists
    assert os.path.exists(w.output_filepath), f"Failed to find output file at {w.export_output_data}"