# imports
import pandas as pd
import os
from functions import log
from validators import EmptyValidator, FilePathValidator
from PyInquirer import Token, ValidationError, Validator, print_json, prompt, style_from_dict


class ModeSelect:

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    def __init__(self):
        self.input_modes = ['postcode', 'sa2', 'sa3', 'suburb']
        self.output_modes = ['state electorates', 'federal electorates']
        self.questions = None
        self.answers = None
        self.input_mode = None
        self.output_mode = None

    def set_questions(self):
        self.questions = [
            {
                'type': 'list',
                'name': 'input_mode',
                'message': 'What is the geography of your input file?',
                'choices': self.input_modes,
                'validate': EmptyValidator
            },
            {
                'type': 'list',
                'name': 'output_mode',
                'message': 'What geography do you want to output?',
                'choices': self.output_modes,
                'validate': EmptyValidator
            }
        ]

    def get_answers(self):
        self.answers = prompt(self.questions)

    def set_answers(self):
        self.input_mode = self.answers['input_mode']
        self.output_mode = self.answers['output_mode']

    def prompt(self):
        self.set_questions()
        self.get_answers()
        self.set_answers()


class RunOptions:

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    def __init__(self):
        self.questions = None
        self.answers = None
        self.set_questions()

    def set_questions(self):
        self.questions = [
            {
                'type': 'input',
                'name': 'input_file',
                'message': 'Please enter the file path to your input file',
                'default': 'test-data/2016Census_G01_AUS_POA_diff_name.csv',
                'validate': FilePathValidator
            }, {
                'type': 'input',
                'name': 'input_join_column',
                'message': 'What is the name of the geography column in your file? (e.g, POA_CODE_2016)',
                'default': 'POA_CODE_2016',
                'validate': EmptyValidator
            }, {
                'type': 'input',
                'name': 'input_numerator_column',
                'message': 'What property do you want to calculate? (numerator, e.g Counted_Census_Night_home_P)',
                'default': 'Counted_Census_Night_home_P',
                'validate': EmptyValidator
            }, {
                'type': 'input',
                'name': 'input_denominator_column',
                'message': 'What is your total column (denominator, e.g Tot_P_P)',
                'default': 'Tot_P_P',
                'validate': EmptyValidator
            }, {
                'type': 'input',
                'name': 'output_file',
                'message': 'What subfolder do you want to use for your output file',
                'default': 'output',
                'validate': EmptyValidator
            }, {
                'type': 'input',
                'name': 'output_file',
                'message': 'What name do you want to use for your output file',
                'default': 'file.csv',
                'validate': EmptyValidator
            }
        ]

    def get_answers(self):
        self.answers = prompt(self.questions)

    def prompt(self):
        self.set_questions()
        self.get_answers()


class Weights:
    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    def __init__(self, input_mode, output_mode):
        self.input_mode = input_mode
        self.output_mode = output_mode


class Weight:

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    def __init__(self, input_mode, output_mode):
        # mode decider
        self.input_mode = input_mode
        self.output_mode = output_mode

        # properties for input file
        # filepath
        self.input_file = None
        # column to join to weight on
        self.input_join_column = None
        # column to calc % from (numerator)
        self.input_numerator_column = None
        # column to calc % from (denominator)
        self.input_denominator_column = None

        # properties for weight file
        # filepath
        self.weight_file = None
        # column to join to input on
        self.weight_join_column = None
        # column with pretty name for output
        self.weight_name_column = None
        # column with population weight value
        self.weight_proportion_overlap_column = None

        # placeholder vars
        self.weight_file = None
        self.weight_data = None
        self.process_data = None
        self.output_data = None

        # settings
        self.output_dir = 'output'
        self.output_file = 'file.csv'
        self.output_filepath = None

        # need a neater way to do this - basically, if you are postcode-state, we want to
        if self.input_mode == 'postcode' and self.output_mode == 'state electorates':
            self.postcode_state()
        elif self.input_mode == 'postcode' and self.output_mode == 'federal electorates':
            self.postcode_federal()
        else:
            log('Sorry, this combination of input and output modes is not implemented yet!', color='red')

        self.debug = False

    # update several properties of the class with vals (eg from cmd line tool)
    def update_properties(self, data):
        for name, value in data.items():
            setattr(self, name, value.strip())

    # if weighting postcode and state, this is the weight data you need
    def set_weight_data_postcode_state(self):
        self.update_properties({
            'weight_file': 'weight-data/poa_2016_sed_2013_concordance_vic_nonflat.csv',
            'weight_join_column': 'POA_CODE_2016',
            'weight_name_column': 'district',
            'weight_proportion_overlap_column': 'proportion_in_district'
        })

    def set_weight_data_postcode_federal(self):
        self.update_properties({
            'weight_file': 'weight-data/poa_2016_ced_2016_concordance_aust_nonflat.csv',
            'weight_join_column': 'postcode',
            'weight_name_column': 'ced_2016',
            'weight_proportion_overlap_column': 'proportion_in_ced_2016'
        })

    # if postcode_state, set those weights

    def postcode_state(self):
        self.set_weight_data_postcode_state()

    def postcode_federal(self):
        self.set_weight_data_postcode_federal()

    def get_input_data(self):
        self.input_data = pd.read_csv(self.input_file)

    def get_weight_data(self):
        self.weight_data = pd.read_csv(self.weight_file)

    def run_merge_data(self):
        self.process_data = pd.merge(self.weight_data, self.input_data, how='left',
                                     left_on=self.weight_join_column, right_on=self.input_join_column)

        if self.debug:
            self.process_data.to_csv('debug/merge_data.csv')

    def add_total_column(self):
        self.process_data[f'{self.input_denominator_column}_total'] = self.process_data[self.input_denominator_column] * \
            self.process_data[self.weight_proportion_overlap_column]

    def run_process_data(self):
        # add total
        self.add_total_column()

        # add numeric column
        self.process_data[f'{self.input_numerator_column}_n'] = self.process_data[self.input_numerator_column] * \
            self.process_data[self.weight_proportion_overlap_column]
        self.process_data[self.input_denominator_column] = self.process_data[self.input_denominator_column]

        if self.debug:
            self.process_data.to_csv('debug/process_data.csv')

    def run_cull_data(self):
        # group by, add up, reset index to get a data frame, limit to sensible columns, export
        self.output_data = self.process_data[[
            self.weight_name_column, self.weight_join_column, f'{self.input_numerator_column}_n', f'{self.input_denominator_column}_total']]
        self.output_data = self.output_data.groupby(
            [self.weight_name_column]).sum()
        self.output_data = self.output_data.reset_index()
        self.output_data[f'{self.input_numerator_column}_pc'] = self.output_data[f'{self.input_numerator_column}_n'] / \
            self.output_data[f'{self.input_denominator_column}_total']
        self.output_data = self.output_data[[
            self.weight_name_column, f'{self.input_numerator_column}_n', f'{self.input_numerator_column}_pc', f'{self.input_denominator_column}_total']]

    def set_output_filepath(self):
        self.output_filepath = self.output_dir + os.sep + self.output_file

    def export_output_data(self):
        self.set_output_filepath()
        self.output_data.to_csv(self.output_filepath, index=False)

    def run(self):
        # load data
        self.get_input_data()
        self.get_weight_data()
        # process
        self.run_merge_data()
        self.run_process_data()
        self.run_cull_data()
        # export
        self.export_output_data()
