import os
import shutil
from rpy2 import robjects
from rpy2.robjects.conversion import localconverter
from rpy2.robjects import pandas2ri, default_converter

DoBMIQ_path = './R Scripts/DoBMIQ.R'
wd_path = './'
lib_paths = './R Scripts/packages'

def r_environment_setup(wd_path, lib_path):
    try:
        print("Entering r_environment_setup")
        working_directory = os.path.abspath(wd_path).replace("\\", "/")
        print(f"Resolved working directory: {working_directory}")

        # Set working directory in R
        robjects.r(f'setwd("{working_directory}")')
        print(f"Working directory set to: {working_directory}")

        # Set library path in R
        robjects.r(f'.libPaths("{lib_path}")')
        print(f"Library path set to: {lib_path}")

        # Test R environment setup by running a simple command
        robjects.r('print("R environment setup successful")')
    except Exception as e:
        print(f"Error in r_environment_setup: {e}")
        raise

def call_DoBMIQ(probe_path, beta_path):
    try:
        print(f"Calling DoBMIQ with:\n  Probe path: {probe_path}\n  Beta path: {beta_path}")
        print(f"DoBMIQ path: {os.path.abspath(DoBMIQ_path)}")

        robjects.r(f'source("{DoBMIQ_path}")')
        print("DoBMIQ script sourced successfully")
        print(f"Working directory in R: {robjects.r('getwd()')}")

        DoBMIQ = robjects.globalenv['DoBMIQ']
        DoBMIQ(probe_path, beta_path)
        print("DoBMIQ executed successfully")
    except Exception as e:
        print(f"Error in call_DoBMIQ: {e}")
        raise

def compress_results_folder(result_path, output_path):
    try:
        result_path = os.path.abspath(result_path)
        output_path = os.path.abspath(output_path)

        shutil.make_archive(output_path, 'zip', result_path)
        print(f"Successfully compressed results folder to {output_path}.zip")
    except Exception as e:
        print("Error compressing results folder: ", e)
        raise e

def compute_results(probe_data_path, beta_data_path):
    print(f"compute_results called with:\n  Probe data path: {probe_data_path}\n  Beta data path: {beta_data_path}")

    try:
        print("Activating pandas2ri conversion")
        with localconverter(default_converter):
            pandas2ri.activate()
            print("Pandas2ri conversion activated")

            # Step 1: Set up R environment
            print("Setting up R environment")
            r_environment_setup(wd_path, lib_paths)

            # Step 2: Call the DoBMIQ R script
            print("Calling DoBMIQ script")
            call_DoBMIQ(probe_data_path, beta_data_path)

            # Step 3: Compress results folder
            print("Compressing results folder")
            compress_results_folder("./R Scripts/results", "./R Scripts/results")

            print("compute_results completed successfully")
        pandas2ri.deactivate()
        print("Pandas2ri conversion deactivated")
    except Exception as e:
        print(f"Error in compute_results: {e}")
        raise

probe_data_path = './R Scripts/data/probesample.xlsx'
beta_data_path = './R Scripts/data/beta.xlsx'
# beta_data_path = './R Scripts/data/beta(working).xlsx'


# probe_data_path = '../uploads/probesample.xlsx'
# beta_data_path = '../uploads/beta.xlsx'

compute_results(probe_data_path, beta_data_path)