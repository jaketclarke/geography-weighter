# imports
import pandas as pd

# input variables
input_file = 'test-data/2016Census_G01_AUS_POA.csv'
input_mode = 'postcode'
input_join_column = 'POA_CODE_2016'

# mode decider
output_mode = 'state'

# postcode state mode config
# ship off to config file?
postcode_state_weight_file = 'test-data/poa_2016_sed_2013_concordance_vic_nonflat.csv'
postcode_state_join_column = 'POA_CODE_2016'
postcode_state_name_column = 'district'
postcode_state_weight_column = 'proportion_in_district'

# hello world - load the input and output files and dump to console

input_data = pd.read_csv(input_file)
weight_data = pd.read_csv(postcode_state_weight_file)

print(input_data.head(10))
print(weight_data.head(10))