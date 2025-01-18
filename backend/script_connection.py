import os
import shutil
from rpy2 import robjects
from rpy2.robjects.conversion import localconverter
from rpy2.robjects import pandas2ri, default_converter

DoBMIQ_path = './DoBMIQ.R'
wd_path = './R Scripts'
lib_paths = 'packages'

def r_environment_setup(wd_path, lib_path):
    try:
        print("Setting up R environment")
        working_directory = os.path.abspath(wd_path)
        
        with localconverter(default_converter):
            robjects.r(f'setwd("{working_directory}")')
            print(f"Working directory set to: {working_directory}")

            robjects.r(f'.libPaths("{lib_path}")')
            print(f"Library path set to: {lib_path}\n")
    except Exception as e:
        print("Error setting R environment: ", e)
        raise e

def call_DoBMIQ(probe_path, beta_path):
    try:
        with localconverter(default_converter):
            DoBMIQ_abs_path = os.path.abspath(DoBMIQ_path)
            robjects.r(f'source("{DoBMIQ_abs_path}")')
            DoBMIQ = robjects.globalenv['DoBMIQ']
            DoBMIQ(probe_path, beta_path)
            print("Successfully executed DoBMIQ")
    except Exception as e:
        print("Error executing DoBMIQ: ", e)
        raise e

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
    # global progress_state

    # Initialize the R converter at the start of the function
    with localconverter(default_converter):
        pandas2ri.activate()
        
        try:
            # progress_state["status"] = "Setting up R environment"
            # progress_state["progress"] = 10
            r_environment_setup(wd_path, lib_paths)

            # progress_state["status"] = "Running DoBMIQ..."
            # progress_state["progress"] = 50
            call_DoBMIQ(probe_data_path, beta_data_path)

            # progress_state["status"] = "Compressing results..."
            # progress_state["progress"] = 90
            compress_results_folder("./results", "./results")

            # progress_state["status"] = "Completed!"
            # progress_state["progress"] = 100
        # except Exception as e:
        #     progress_state["status"] = f"Error: {str(e)}"
        #     progress_state["progress"] = -1
        #     raise e
        finally:
            pandas2ri.deactivate()

# probe_data_path = './R Scripts/data/probesample.xlsx'
# beta_data_path = './R Scripts/data/beta.xlsx'

probe_data_path = '../uploads/probesample.xlsx'
beta_data_path = '../uploads/beta.xlsx'

# compute_results(probe_data_path, beta_data_path)