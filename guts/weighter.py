# imports
import json
import logging
import os
import pandas as pd
import numpy as np
from warnings import simplefilter
from PyInquirer import prompt
from .functions import make_directorytree_if_not_exists
from .validators import EmptyValidator

# disable a performance warning
simplefilter(action="ignore", category=pd.errors.PerformanceWarning)


class SelectInputFile:
    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    def __init__(self):
        self.input_file = None
        self.input_data = None

    def set_questions(self):
        self.questions = [
            {
                "type": "input",
                "name": "input_file",
                "message": "What is the path to your input file?",
                "validate": EmptyValidator,
            }
        ]

    def get_answers(self):
        self.answers = prompt(self.questions)

    def set_answers(self):
        self.input_file = self.answers["input_file"]

    def prompt(self):
        self.set_questions()
        self.get_answers()
        self.set_answers()


class ModeSelect:
    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    def __init__(self):
        self.input_modes = ["postcode", "sa1", "sa1-2021", "sa2", "sa3", "suburb"]
        self.output_modes = ["state electorates", "federal electorates"]
        self.questions = None
        self.answers = None
        self.input_mode = None
        self.output_mode = None

    def set_questions(self):
        self.questions = [
            {
                "type": "list",
                "name": "input_mode",
                "message": "What is the geography of your input file?",
                "choices": self.input_modes,
                "validate": EmptyValidator,
            },
            {
                "type": "list",
                "name": "output_mode",
                "message": "What geography do you want to output?",
                "choices": self.output_modes,
                "validate": EmptyValidator,
            },
        ]

    def get_answers(self):
        self.answers = prompt(self.questions)

    def set_answers(self):
        self.input_mode = self.answers["input_mode"]
        self.output_mode = self.answers["output_mode"]

    def prompt(self):
        self.set_questions()
        self.get_answers()
        self.set_answers()


class RunOptions:
    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    def __init__(self, input_file_headers):
        self.questions = None
        self.answers = None
        self.input_file_headers = input_file_headers
        self.input_file_headers_dict = []

    def get_numerator_options(self):
        for header in self.input_file_headers:
            self.input_file_headers_dict.append({"name": header, "checked": True})

    def set_questions(self):
        self.questions = [
            {
                "type": "list",
                "name": "input_join_column",
                "message": (
                    "What is the name of the geography column in your file? (e.g, POA_CODE_2016)"
                ),
                "choices": self.input_file_headers,
                "validate": EmptyValidator,
            },
            {
                "type": "checkbox",
                "name": "input_numerator_columns",
                "message": (
                    "What properties do you want to calculate? (numerator, e.g"
                    " Counted_Census_Night_home_P)"
                ),
                "choices": self.input_file_headers_dict,
                "validate": EmptyValidator,
            },
            {
                "type": "input",
                "name": "input_denominator_column",
                "message": "What is your total column (denominator, e.g Tot_P_P)",
                "default": "Tot_P_P",
                "validate": EmptyValidator,
            },
            {
                "type": "input",
                "name": "output_dir",
                "message": "What subfolder do you want to use for your output file",
                "default": "output",
                "validate": EmptyValidator,
            },
            {
                "type": "input",
                "name": "output_file",
                "message": "What prefix do you want to use for your output files?",
                "default": "file",
                "validate": EmptyValidator,
            },
        ]

    def get_answers(self):
        self.answers = prompt(self.questions)

    def prompt(self):
        self.get_numerator_options()
        self.set_questions()
        self.get_answers()


class Weight:
    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    def __init__(self, input_mode, output_mode, input_file):
        # mode decider
        self.input_mode = input_mode
        self.output_mode = output_mode
        self.input_file = input_file

        # weight configuration
        self.weight_config_file = "weight-data/weight_config.json"

        # properties for input file
        # filepath\
        # column to join to weight on
        self.input_join_column = None
        # column to calc % from (numerator)
        # self.input_numerator_column = None
        # trying to handle multiple columns
        self.input_numerator_columns = ["Tot_P_M", "Tot_P_F"]
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
        self.output_data_unpivoted = None

        # settings
        self.output_dir = "output"
        self.output_file = "file"
        self.output_filepath = None

        # make output dir if not exists
        self.create_output_directory_if_not_exists()

        # the loading of weight options should come from the file system
        # this should get broken into an input mode/set weights class
        # the weights class should just get the input data for readability

        self.load_weight_options()
        # break this into another func/class with the input mode stuff
        self.set_weight_data()

        self.debug = False

    # update several properties of the class with vals (eg from cmd line tool)
    def create_output_directory_if_not_exists(self):
        """Create a directory if it does not exist

        Args:
            directory (str): path to directory
        """
        try:
            if not os.path.exists(self.output_dir):
                os.makedirs(self.output_dir)
                print(f"created {self.output_dir}")
        except RuntimeError:
            f"Could not create output directory {self.output_dir}"

    def update_properties(self, data):
        for name, value in data.items():

            # ToDo strip white space from value if not list
            setattr(self, name, value)

    def set_weight_data(self):
        try:
            weight_key = f"{self.input_mode}_{self.output_mode}"
            weight_data = self.weight_definitions[weight_key]
            self.update_properties(weight_data)

        except LookupError:
            f"There is not a weight implementation for {self.input_mode} and {self.output_mode}"

    def load_weight_options(self):
        try:
            with open(self.weight_config_file, "r") as f:
                self.weight_definitions = json.loads(f.read())
        # ToDO error logger
        except ImportError:
            f"There is not a properly formatted config file at {self.weight_config_file}"

    def get_input_data(self):
        self.input_data = pd.read_csv(self.input_file, na_values=["Null", "NaN", "nan", "Nan"])

    def get_weight_data(self):
        self.weight_data = pd.read_csv(self.weight_file, na_values=["Null", "NaN", "nan", "Nan"])

    def run_merge_data(self):
        self.process_data = pd.merge(
            self.weight_data,
            self.input_data,
            how="left",
            left_on=self.weight_join_column,
            right_on=self.input_join_column,
        )

        if self.debug:
            make_directorytree_if_not_exists("debug")
            self.process_data.to_csv("debug/merge_data.csv", index=False, na_rep="Null")

    def add_total_column(self):
        self.process_data[f"{self.input_denominator_column}_total"] = (
            self.process_data[self.input_denominator_column]
            * self.process_data[self.weight_proportion_overlap_column]
        )

    def run_process_data(self):
        # update types
        # convert to floats
        
        self.process_data[self.weight_proportion_overlap_column] = pd.to_numeric(self.process_data[self.weight_proportion_overlap_column])
        self.process_data[self.input_denominator_column] = pd.to_numeric(self.process_data[self.input_denominator_column])
        

        # add total
        self.add_total_column()

        for col in self.input_numerator_columns:
            self.process_data[f"{col}"] = pd.to_numeric(self.process_data[f"{col}"])
            
            self.process_data[f"{col}"] = (
                self.process_data[col] * self.process_data[self.weight_proportion_overlap_column]
            )

        self.process_data[self.input_denominator_column] = self.process_data[
            self.input_denominator_column
        ]

        if self.debug:
            make_directorytree_if_not_exists("debug")
            self.process_data.to_csv("debug/process_data.csv", index=False, na_rep="Null")

    def run_cull_data(self):
        # group by, add up, reset index to get a data frame, limit to sensible columns, export
        process_data_properties = [self.weight_name_column, self.weight_join_column]

        for col in self.input_numerator_columns:
            if col != self.input_join_column:
                process_data_properties.append(f"{col}")

        process_data_properties.append(f"{self.input_denominator_column}_total")
        self.output_data = self.process_data[process_data_properties]
        # if the entire column is NaN, min count below will ensure the output is NaN
        # this is put in because the 2021 census data has some data not released at the sa1 level
        self.output_data = (
            self.output_data.groupby([self.weight_name_column]).sum(min_count=1).round(0)
        )
        self.output_data = self.output_data.reset_index()

        for col in self.input_numerator_columns:
            if col != self.input_join_column:
                # ToDo  PerformanceWarning: DataFrame is highly fragmented.
                # This is usually the result of calling `frame.insert` ...

                self.output_data[f"{col}_pc"] = (
                    self.output_data[f"{col}"]
                    / self.output_data[f"{self.input_denominator_column}_total"]
                ).round(4)

        keep = [self.weight_name_column]
        for col in self.input_numerator_columns:
            if col != self.input_join_column:
                keep.append(f"{col}")
                keep.append(f"{col}_pc")
        keep.append(f"{self.input_denominator_column}_total")
        self.output_data = self.output_data[keep]

    def export_output_data(self):
        path = self.output_dir + os.sep + self.output_file + ".csv"
        self.output_data.to_csv(path, index=False, na_rep="Null")

    def export_output_data_unpivoted(self):
        path = self.output_dir + os.sep + f"{self.output_file}_unpivoted" + ".csv"
        # gets the name of the output data column from the first column of the input data, e.g, district, electorate, etc
        label = self.output_data.columns[0]
        self.output_data_unpivoted = self.output_data.melt(
            id_vars=label, var_name="census_variable", value_name="value"
        )
        self.output_data_unpivoted.to_csv(path, index=False, na_rep="Null")

    def export_output_data_pc(self):
        df = self.output_data
        # keep the label and all columns ending in pc
        keep_cols = [df.columns[0]]
        for col in df.columns:
            if "_pc" in col:
                keep_cols.append(col)
        out = df[df.columns[df.columns.isin(keep_cols)]]
        path = self.output_dir + os.sep + f"{self.output_file}_pc" + ".csv"
        out.to_csv(path, index=False, na_rep="Null")

    def export_output_data_n(self):
        df = self.output_data
        out = df[df.columns[~df.columns.str.endswith("_pc")]]
        path = self.output_dir + os.sep + f"{self.output_file}_n" + ".csv"
        out.to_csv(path, index=False, na_rep="Null")

    def run_ranking(self):
        # gets the name of the output data column from the first column of the input data, e.g, district, electorate, etc
        geography_label = self.output_data.columns[0]

        # path to unpivoted data
        path = self.output_dir + os.sep + f"{self.output_file}_unpivoted" + ".csv"

        # get data
        input_data = pd.read_csv(path, na_values=["Null", "NaN", "nan", "Nan"])

        # order for ranking
        input_data.sort_values(by=["census_variable", "value"], inplace=True)

        # rank
        tmp = input_data.groupby("census_variable").size()
        rank = tmp.map(range)
        rank = [item for sublist in rank for item in sublist]
        input_data["rank"] = rank
        input_data["rank"] = input_data["rank"] + 1

        # if all the input data is NaN, don't rank
        input_data.loc[input_data["value"].isnull(), "rank"] = np.nan

        output_file = path.replace("unpivoted", "ranked_unpivoted")
        input_data.to_csv(output_file, index=False, na_rep="Null")

        # repivot
        transform = pd.pivot_table(data=input_data, index=[geography_label, "census_variable"])
        transform = transform.reset_index()
        try:
            transform.drop(columns="value", inplace=True)
        except:
            logging.info("couldn't drop columns in transformation")

        pivot = transform.pivot(index=geography_label, columns="census_variable", values="rank")
        output_file = path.replace("unpivoted", "ranked")
        pivot.to_csv(output_file, na_rep="Null")

        print(f"processed {output_file} \r\n")

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
        # export unpivoted data
        self.export_output_data_unpivoted()

        self.export_output_data_pc()
        self.export_output_data_n()
        self.run_ranking()
