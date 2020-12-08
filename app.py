# libraries
import json
import os
import sys
from functions import *
from weighter import *
from pyfiglet import Figlet
from clint.arguments import Args
from clint.textui import puts, indent, colored
import click
from PyInquirer import Token, ValidationError, Validator, print_json, prompt, style_from_dict


class EmptyValidator(Validator):
    def validate(self, value):
        if len(value.text):
            return True
        else:
            raise ValidationError(
                message="You can't leave this blank",
                cursor_position=len(value.text))


class FilePathValidator(Validator):
    def validate(self, value):
        if len(value.text):
            if os.path.isfile(value.text):
                return True
            else:
                raise ValidationError(
                    message="File not found",
                    cursor_position=len(value.text))
        else:
            raise ValidationError(
                message="You can't leave this blank",
                cursor_position=len(value.text))


@click.command()
def main():
    log("Geographic Weighter", color="green", figlet=True)
    log("Welcome to the Geographic Weighter", "green")
    log("This tool will take an input file with properties for a geography, such as census data by postcode, and output it by a different geography, for example federal electorates", "green")
    log("This process calculates population weighted percentages for the input fields, so requires a numeric input for each property, as well as a total population column for the area", "green")
    log("To get started, enter the path to your file below:", "green")

    # Work out what kind of geography we are dealing with
    qtype = [
        {
            'type': 'list',
            'name': 'input_mode',
            'message': 'What is the geography of your input file?',
            'choices': ['postcode', 'sa2', 'sa3', 'suburb'],
            'validate': EmptyValidator
        },
        {
            'type': 'list',
            'name': 'output_mode',
            'message': 'What geography do you want to output?',
            'choices': ['state electorates', 'federal electorates'],
            'validate': EmptyValidator
        }
    ]

    atype = prompt(qtype)

    # initialise a weight object with the geog type specified
    w = Weight(input_mode=atype['input_mode'],
               output_mode=atype['output_mode'])

    # ask questions to do the weighting
    questions = [
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
        }
    ]

    # ask questions
    answers = prompt(questions)

    # update weight class with data entered
    w.update_properties(answers)

    # implement postcode / state electorate
    # replace below with a call to the class
    if w.input_mode == 'postcode' and w.output_mode == 'state electorates':
        # load data
        w.get_input_data()
        w.get_weight_data()
        # process
        w.run_merge_data()
        w.run_process_data()
        w.run_cull_data()
        # export
        w.export_output_data()
    else:
        log(f"Unfortunately weighting {w.input_mode} by {w.output_mode} is not implemented yet", color="red")


if __name__ == '__main__':
    main()
