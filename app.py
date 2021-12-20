# libraries
import json
import os
import sys

import pandas as pd
from guts.functions import *
from guts.weighter import ModeSelect, Weight, RunOptions, SelectInputFile
from pyfiglet import Figlet
from clint.arguments import Args
from clint.textui import puts, indent, colored
import click
from PyInquirer import Token, ValidationError, Validator, print_json, prompt, style_from_dict
from guts.validators import EmptyValidator, FilePathValidator


@click.command()
def main():
    log("Geographic Weighter", color="green", figlet=True)
    log("Welcome to the Geographic Weighter", "green")
    log("This tool will take an input file with properties for a geography, such as census data by postcode, and output it by a different geography, for example federal electorates", "green")
    log("This process calculates population weighted percentages for the input fields, so requires a numeric input for each property, as well as a total population column for the area", "green")
    log("To get started, enter the path to your file below:", "green")

    file = SelectInputFile()
    file.prompt()

    mode = ModeSelect()
    mode.prompt()

    data = pd.read_csv(file.input_file)

    # initialise a weight object with the geog type specified
    w = Weight(input_mode=mode.input_mode,
               output_mode=mode.output_mode,
               input_file=file.input_file)

    # get data - #MAKE THIS A FUNCTION
    input_file_headers = data.columns.values
    options = RunOptions(input_file_headers)
    options.prompt()

    # update weight class with data entered
    w.update_properties(options.answers)

    # implement postcode / state electorate
    # replace below with a call to the class
    # try:
    w.run()
    # except:
    #     log(f"Unfortunately, something went wrong", color="red")
    #     log(f"{w}", color='green')


if __name__ == '__main__':
    main()
