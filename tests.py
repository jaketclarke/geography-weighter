from weighter import *
import pytest
import os

# tests for strip_parent_directory
def test_weight_run():
    w = Weight()
    w.get_input_data()
    w.get_weight_data()
    w.run_merge_data()
    w.run_process_data()
    w.run_cull_data()
    w.export_output_data()
    assert os.path.exists(w.output_filepath), f"Failed to find output file at {w.export_output_data}"