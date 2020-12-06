# libraries
import json
import os
import argparse
import sys
from functions import *
from weighter import *

# set up console interface
parser = argparse.ArgumentParser(description='Weighter\r\nSome sensible description can go here')
required = parser.add_argument_group('required arguments')
parser.add_argument('--input-file', default='test-data/2016Census_G01_AUS_POA.csv', dest='input_file', type=str, help='The file you want to weight data for')
# parser.add_argument('--output-dir', default='output', dest='outputdir', type=str, help='Directory to save JSON files to')
# required.add_argument('--key', dest='key', type=str, help='Key to add to the JSON')
# required.add_argument('--value', dest='value', type=str, help='Value to add to the JSON')

args = parser.parse_args()

input_input_file = args.input_file
print(input_input_file)
# if not args.value:
#     print("Please specify the value you wish to add to the JSON")
#     parser.print_help()
#     sys.exit(2)

# set values
# directoryinput = args.inputdir
# directoryoutput = args.outputdir
# key = args.key
# value = args.value

# run the weighting
w = Weight()
# ensure output dir exists
make_directorytree_if_not_exists(w.output_dir)
# load data
w.get_input_data()
w.get_weight_data()
# process
w.run_merge_data()
w.run_process_data()
w.run_cull_data()
# export
w.export_output_data()
# check export file exists
assert os.path.exists(w.output_filepath), f"Failed to find output file at {w.export_output_data}"