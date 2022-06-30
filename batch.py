import pandas as pd

from guts.functions import log
from guts.weighter import ModeSelect, RunOptions, SelectInputFile, Weight


input_mode = 'sa1-2021'
output_mode = 'state electorates'
output_file = 'testabc.csv'
input_join_column = 'SA1_CODE_2021'
input_numerator_columns = ''
input_denominator_column = 'Total_Total'
# for file in data

input_file = 'data/2021Census_G03_AUST_SA1.csv'
data = pd.read_csv(input_file)

# initialise a weight object with the geog type specified
weight = Weight(
    input_mode = input_mode,
    output_mode = output_mode,
    input_file = input_file
)

# get data - #MAKE THIS A FUNCTION
input_file_headers = data.columns.values
input_numerator_columns = input_file_headers

answers = {
    'output_file': output_file,
    'input_join_column': input_join_column,
    'input_numerator_columns': input_numerator_columns,
    'input_denominator_column': input_denominator_column
}

# update weight class with data entered
weight.update_properties(answers)

weight.run()
