import pandas as pd
import os
from guts.functions import log, get_files_in_directory
from guts.weighter import ModeSelect, RunOptions, SelectInputFile, Weight


# settings
input_mode = 'sa1-2021'
output_mode = 'state electorates'
input_join_column = 'SA1_CODE_2021'
input_denominator_column = 'P_Tot_Tot'

# get files to process
input_files = get_files_in_directory(f'data{os.sep}')

print(input_files)

for input_file in input_files:

    print(f'starting to process {input_file}\r\n')
    
    output_file = input_file.replace('AUST_SA1.csv', 'VIC_SED_2022') # the output adds .csv on to the extension
    input_file = 'data' + os.sep + input_file

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

    print(f'processed {output_file}\r\n')
