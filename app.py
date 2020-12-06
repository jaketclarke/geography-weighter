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

config = {}

@click.command()
def main():
    """
    Simple CLI for sending emails using SendGrid
    """
    log("Geographic Weighter", color="green", figlet=True)
    log("Welcome to the Geographic Weighter", "blue")
    
    questions = [
        {
            'type': 'input',
            'name': 'first_name',
            'message': 'What\'s your first name',
        }
    ]
    answers = prompt(questions)
    print(answers)

if __name__ == '__main__':
    main()


# # set up console interface
# # parser = argparse.ArgumentParser(description='Weighter\r\nSome sensible description can go here')
# # required = parser.add_argument_group('required arguments')
# # parser.add_argument('--input-file', default='test-data/2016Census_G01_AUS_POA.csv', dest='input_file', type=str, help='The file you want to weight data for')
# # # parser.add_argument('--output-dir', default='output', dest='outputdir', type=str, help='Directory to save JSON files to')
# # # required.add_argument('--key', dest='key', type=str, help='Key to add to the JSON')
# # # required.add_argument('--value', dest='value', type=str, help='Value to add to the JSON')

# # args = parser.parse_args()

# # input_input_file = args.input_file
# # print(input_input_file)
# # if not args.value:
# #     print("Please specify the value you wish to add to the JSON")
# #     parser.print_help()
# #     sys.exit(2)

# # set values
# # directoryinput = args.inputdir
# # directoryoutput = args.outputdir
# # key = args.key
# # value = args.value

# # run the weighting
# w = Weight()
# # ensure output dir exists
# make_directorytree_if_not_exists(w.output_dir)
# # load data
# w.get_input_data()
# w.get_weight_data()
# # process
# w.run_merge_data()
# w.run_process_data()
# w.run_cull_data()
# # export
# w.export_output_data()
# # check export file exists
# assert os.path.exists(w.output_filepath), f"Failed to find output file at {w.export_output_data}"