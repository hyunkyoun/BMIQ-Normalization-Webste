import os
import shutil
from rpy2 import robjects
from rpy2.robjects.conversion import localconverter
from rpy2.robjects import pandas2ri

DoBMIQ_path = './DoBMIQ.R'
wd_path = './R Scripts'
lib_paths = 'packages'

# This is a function to set up the R environment. 
def r_environment_setup(wd_path, lib_path):
    try:
        print("Setting up R environment")

        working_directory = os.path.abspath(wd_path)

        robjects.r(f'setwd("{working_directory}")')
        print(f"Working directory set to: {working_directory}")

        robjects.r(f'.libPaths("{lib_path}")')
        print(f"Library path set to: {lib_path}\n")
    except Exception as e:
        print("Error setting R environment: ", e)

# This is a function to call the DoBMIQ function from the DoBMIQ.R script
def call_DoBMIQ(probe_path, beta_path):
    try:
        DoBMIQ_abs_path = os.path.abspath(DoBMIQ_path)

        robjects.r(f'source("{DoBMIQ_abs_path}")')
        DoBMIQ = robjects.globalenv['DoBMIQ']

        DoBMIQ(probe_path, beta_path)

        print("Successfully executed DoBMIQ")

    except Exception as e:
        print("Error executing DoBMIQ: ", e)
        raise

# This is a function to compress the results
def compress_results_folder(result_path, output_path):
    try:
        result_path = os.path.abspath(result_path)
        output_path = os.path.abspath(output_path)

        shutil.make_archive(output_path, 'zip', result_path)
        print(f"Successfully compressed results folder to {output_path}.zip")
    except Exception as e:
        print("Error compressing results folder: ", e)



# This is the function to get the results from the user inputted xlsx files. 
def compute_results(probe_data_path, beta_data_path):
    r_environment_setup(wd_path, lib_paths)
    call_DoBMIQ(probe_data_path, beta_data_path)
    compress_results_folder("./results", "./results")

# probe_data_path = './data/probesample.xlsx'
# beta_data_path = './data/beta.xlsx'
probe_data_path = '../uploads/probesample.xlsx'
beta_data_path = '../uploads/beta.xlsx'

# compute_results(probe_data_path, beta_data_path)