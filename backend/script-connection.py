from rpy2 import robjects
import os
import shutil

DoBMIQ_path = './DoBMIQ.R'
probe_data_path = './data/probesample.xlsx'
beta_data_path = './data/beta.xlsx'
wd_path = './R Scripts'
lib_paths = 'packages'

def r_environment_setup(wd_path, lib_path):
    try:
        print("Setting up R environment")

        working_directory = os.path.abspath(wd_path)
        # lib_path = os.path.abspath(lib_paths)

        robjects.r(f'setwd("{working_directory}")')
        print(f"Working directory set to: {working_directory}")

        robjects.r(f'.libPaths("{lib_path}")')
        print(f"Library path set to: {lib_path}\n")
    except Exception as e:
        print("Error setting R environment: ", e)

def call_DoBMIQ(probe_path, beta_path):
    try:
        DoBMIQ_abs_path = os.path.abspath(DoBMIQ_path)

        robjects.r(f'source("{DoBMIQ_abs_path}")')
        DoBMIQ = robjects.globalenv['DoBMIQ']
        DoBMIQ(probe_path, beta_path)

        print("Successfully executed DoBMIQ")
    except Exception as e:
        print("Error executing DoBMIQ: ", e)


def compress_results_folder(result_path, output_path):
    try:
        result_path = os.path.abspath(result_path)
        output_path = os.path.abspath(output_path)

        shutil.make_archive(output_path, 'zip', result_path)
        print(f"Successfully compressed results folder to {output_path}.zip")
    except Exception as e:
        print("Error compressing results folder: ", e)


r_environment_setup(wd_path, lib_paths)
call_DoBMIQ(probe_data_path, beta_data_path)
compress_results_folder("./results", "./results")