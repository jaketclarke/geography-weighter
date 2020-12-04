# imports
import pandas as pd

# input variables
input_file = 'test-data/2016Census_G01_AUS_POA.csv'
input_mode = 'postcode'
input_join_column = 'POA_CODE_2016'
input_numerator_column = 'Counted_Census_Night_home_P'
input_denominator_column = 'Tot_P_P'

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

# print(input_data.head(10))
# print(weight_data.head(10))

# left join the data
middle_data = pd.merge(weight_data, input_data, how='left', left_on=postcode_state_join_column, right_on=input_join_column)
# print(middle_data.head(15))

# make weight column
middle_data[input_numerator_column] = middle_data[input_numerator_column] * middle_data[postcode_state_weight_column]
middle_data[input_denominator_column] = middle_data[input_denominator_column]

# print(middle_data.head(15))

# group by
output_data = middle_data[[postcode_state_name_column, postcode_state_join_column, input_numerator_column, input_denominator_column]]
# print(output_data.head(10))

# group by, add up, reset index to get a data frame, limit to sensible columns, export
output = output_data.groupby([postcode_state_name_column]).sum()
output = output.reset_index()
output = output[[postcode_state_name_column, input_numerator_column]]
output.to_csv('output.csv',index=False)
