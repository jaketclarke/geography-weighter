"""
CMD line utilty to do the weighting
"""
import click
import pandas as pd

from guts.functions import log
from guts.weighter import ModeSelect, RunOptions, SelectInputFile, Weight


@click.command()
def main():
    """CMD line utilty to do the weighting"""
    log("Geographic Weighter", color="green", figlet=True)
    log("Welcome to the Geographic Weighter", "green")
    log("This tool takes an input file with properties for an area, eg  data by SA1,", "green")
    log("It then outputs it by a different area, eg by federal electorate", "green")
    log("This process calculates population weighted percentages for the input fields,", "green")
    log("so requires a numeric input for each property,", "green")
    log("as well as a total population column for the area", "green")
    log("To get started, enter the path to your file below:", "green")

    file = SelectInputFile()
    file.prompt()

    mode = ModeSelect()
    mode.prompt()

    data = pd.read_csv(file.input_file)

    # initialise a weight object with the geog type specified
    weight = Weight(
        input_mode=mode.input_mode, output_mode=mode.output_mode, input_file=file.input_file
    )

    # get data - #MAKE THIS A FUNCTION
    input_file_headers = data.columns.values
    options = RunOptions(input_file_headers)
    options.prompt()

    # update weight class with data entered
    weight.update_properties(options.answers)

    # implement postcode / state electorate
    # replace below with a call to the class
    # try:
    weight.run()
    # except:
    #     log(f"Unfortunately, something went wrong", color="red")
    #     log(f"{w}", color='green')


if __name__ == "__main__":
    main()
