# imports
import pandas as pd
import os

class Weight:
    
    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)
    
    def __init__(self, input_mode):
        # input variables
        self.input_file = 'test-data/2016Census_G01_AUS_POA.csv'
        self.input_mode = input_mode
        self.input_join_column = 'POA_CODE_2016'
        self.input_numerator_column = 'Counted_Census_Night_home_P'
        self.input_denominator_column = 'Tot_P_P'

        # mode decider
        self.output_mode = 'state'

        # postcode state mode config
        # ship off to config file?
        self.postcode_state_weight_file = 'test-data/poa_2016_sed_2013_concordance_vic_nonflat.csv'
        self.postcode_state_join_column = 'POA_CODE_2016'
        self.postcode_state_name_column = 'district'
        self.postcode_state_weight_column = 'proportion_in_district'

        # placeholder vars
        self.input_data = None
        self.weight_data = None
        self.process_data = None
        self.output_data = None
        
        # settings
        self.output_dir = 'output'
        self.output_file = 'file.csv'
        self.output_filepath = self.output_dir + os.sep + self.output_file
    
    # update several properties of the class with vals (eg from cmd line tool)
    def update_properties(self, data):
        for name, value in data.items():
            setattr(self, name, value.strip())

    def get_input_data(self):
        self.input_data = pd.read_csv(self.input_file)
    
    def get_weight_data(self):
        self.weight_data = pd.read_csv(self.postcode_state_weight_file)

    def run_merge_data(self):
        self.process_data = pd.merge(self.weight_data, self.input_data, how='left', left_on=self.postcode_state_join_column, right_on=self.input_join_column)

    def run_process_data(self):
        self.process_data[self.input_numerator_column] = self.process_data[self.input_numerator_column] * self.process_data[self.postcode_state_weight_column]
        self.process_data[self.input_denominator_column] = self.process_data[self.input_denominator_column]

    def run_cull_data(self):
        # group by, add up, reset index to get a data frame, limit to sensible columns, export
        self.output_data = self.process_data[[self.postcode_state_name_column, self.postcode_state_join_column, self.input_numerator_column, self.input_denominator_column]]
        self.output_data = self.output_data.groupby([self.postcode_state_name_column]).sum()
        self.output_data = self.output_data.reset_index()
        self.output_data = self.output_data[[self.postcode_state_name_column, self.input_numerator_column]]

    def export_output_data(self):
        self.output_data.to_csv(self.output_filepath,index=False)

class Postcode(Weight):
    def __init__(self):
        self.output_mode = 'provingapoint'
        Weight.__init__(self)