from guts.weighter import Weight
from guts.functions import make_directorytree_if_not_exists
import pytest
import os

# tests for strip_parent_directory


def test_weight_run():
    # create weight class
    w = Weight(input_mode='postcode', output_mode='state electorates', input_file='test_data/2016Census_G01_AUS_POA.csv')

    # simulate the input data from the console
    w.update_properties({
        'input_file': 'test-data/2016Census_G01_AUS_POA.csv',
        'input_join_column': 'POA_CODE_2016',
        'input_numerator_column': 'Counted_Census_Night_home_P',
        'input_denominator_column': 'Tot_P_P',
        'output_file': 'test.csv'
    })

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
    assert os.path.exists(
        w.output_filepath), f"Failed to find output file at {w.export_output_data}"
