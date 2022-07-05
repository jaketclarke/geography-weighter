import pandas as pd
import os
from guts.functions import log, get_files_in_directory
from guts.weighter import ModeSelect, RunOptions, SelectInputFile, Weight
import numpy as np

# get files to process
geography_label = 'district'
input_files = get_files_in_directory(f'output{os.sep}')

for input_file in input_files:
    if 'unpivoted.csv' in input_file and 'ranked' not in input_file:

        print(f'processing {input_file} \r\n')
        # get data
        input_data = pd.read_csv(f'output{os.sep}{input_file}', na_values=['Null','NaN','nan','Nan'])

        # order for ranking
        input_data.sort_values(by=['census_variable', 'value'], inplace=True)

        # rank
        tmp = input_data.groupby('census_variable').size()
        rank = tmp.map(range)
        rank =[item for sublist in rank for item in sublist]
        input_data['rank'] = rank
        input_data["rank"] = input_data["rank"] + 1

        # if all the input data is NaN, don't rank
        input_data.loc[input_data['value'].isnull(), 'rank'] = np.nan

        output_file = input_file.replace('unpivoted','ranked_unpivoted')
        input_data.to_csv(f'output{os.sep}{output_file}', index=False, na_rep='Null')

        # repivot
        transform = pd.pivot_table(data=input_data, index=[geography_label,'census_variable'])
        transform = transform.reset_index()
        transform = transform.drop('value',1)
        
        pivot = transform.pivot(index=geography_label, columns='census_variable',values='rank')
        output_file = input_file.replace('unpivoted','ranked')
        pivot.to_csv(f'output{os.sep}{output_file}', index=False, na_rep='Null')

        print(f'processed {output_file} \r\n')