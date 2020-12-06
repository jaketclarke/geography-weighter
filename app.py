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

# pretty intro text
f = Figlet(font='big')
# print(colored(f.renderText('Geographic Weighter'),'green'))

print(colored.green(f.renderText('Geographic Weighter')))

style = style_from_dict({
    Token.QuestionMark: '#fac731 bold',
    Token.Answer: '#4688f1 bold',
    Token.Instruction: '',  # default
    Token.Separator: '#cc5454',
    Token.Selected: '#0abf5b',  # default
    Token.Pointer: '#673ab7 bold',
    Token.Question: '',
})

args = Args()

with indent(4, quote='>>>'):
    puts(colored.blue('Aruments passed in: ') + str(args.all))
    puts(colored.green('Flags detected: ') + str(args.flags))
    puts(colored.blue('Files detected: ') + str(args.files))
    puts(colored.red('NOT Files detected: ') + str(args.not_files))
    puts(colored.blue('Grouped Arguments: ') + str(dict(args.grouped)))

print()

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
    log("Welcome to the Geographic Weighter", "blue")
    w = Weight()

    questions = [
        {
            'type': 'input',
            'name': 'input_file',
            'message': 'Please enter the file path to your input file',
            'validate': FilePathValidator
        },{
            'type': 'input',
            'name': 'input_mode',
            'message': 'What mode do you want to run?',
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