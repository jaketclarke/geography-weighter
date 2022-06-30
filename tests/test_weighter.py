"""
Tests for guts.weighter
"""
import os

from guts.weighter import Weight


def test_run_weight_class_single_column(ensure_clean_output):
    # pylint: disable=unused-argument
    """
    TEST: will the module work to weight one column from file
    """

    # create weight class
    weight = Weight(
        input_mode="postcode",
        output_mode="state electorates",
        input_file="test_data/2016Census_G01_AUS_POA.csv",
    )

    # simulate the input data from the console
    weight.update_properties(
        {
            "input_file": "test-data/2016Census_G01_AUS_POA.csv",
            "input_join_column": "POA_CODE_2016",
            "input_numerator_columns": ["Counted_Census_Night_home_P"],
            "input_denominator_column": "Tot_P_P",
            "output_file": "test",
        }
    )

    weight.run()

    output_file_one = weight.output_dir + os.sep + weight.output_file + '.csv'
    assert os.path.exists(
        output_file_one
    ), f"Failed to find output file at {weight.export_output_data}"


def test_run_weight_class_multiple_columns(ensure_clean_output):
    # pylint: disable=unused-argument
    """
    TEST: will the module work to weight multiple columns from one file
    """

    # create weight class
    weight = Weight(
        input_mode="postcode",
        output_mode="federal electorates",
        input_file="test_data/2016Census_G01_AUS_POA.csv",
    )

    # simulate the input data from the console
    weight.update_properties(
        {
            "input_file": "test-data/2016Census_G01_AUS_POA.csv",
            "input_join_column": "POA_CODE_2016",
            "input_numerator_columns": ["Counted_Census_Night_home_P", "Tot_P_F"],
            "input_denominator_column": "Tot_P_P",
            "output_file": "test.csv",
        }
    )

    weight.run()
    
    output_file_one = weight.output_dir + os.sep + weight.output_file + '.csv'

    assert os.path.exists(
        output_file_one
    ), f"Failed to find output file at {weight.export_output_data}"
