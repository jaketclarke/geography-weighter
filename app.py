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
    """
    Simple CLI for sending emails using SendGrid
    """
    log("Geographic Weighter", color="green", figlet=True)
    log("Welcome to the Geographic Weighter", "green")
    log("This tool will take an input file with properties for a geography, such as census data by postcode, and output it by a different geography, for example federal electorates", "green")
    log("This process calculates population weighted percentages for the input fields, so requires a numeric input for each property, as well as a total population column for the area", "green")
    log("To get started, enter the path to your file below", "green")
    w = Weight()

    questions = [
        {
            'type': 'input',
            'name': 'input_file',
            'message': 'Please enter the file path to your input file',
            'validate': FilePathValidator
        },{
            'type': 'list',
            'name': 'input_mode',
            'message': 'What is the geography of your input file?',
            'choices': ['postcode','sa2','sa3','suburb'],
            'validate': EmptyValidator
        },{
            'type': 'input',
            'name': 'input_join_column',
            'message': 'What is the name of the geography column in your file? (e.g, POA_CODE_2016)',
            'validate': EmptyValidator
        },{
            'type': 'input',
            'name': 'input_numerator_column',
            'message': 'What property do you want to calculate? (numerator, e.g Counted_Census_Night_home_P)',
            'validate': EmptyValidator
        },{
            'type': 'input',
            'name': 'input_denominator_column',
            'message': 'What is your total column (denominator, e.g Tot_P_P)',
            'validate': EmptyValidator
        }
    ]
    answers = prompt(questions)
    print(answers)

    # overwrite input file
    # w.input_file = answers['input_file']
    w.update_properties(answers)

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

    print(w)

if __name__ == '__main__':
    main()