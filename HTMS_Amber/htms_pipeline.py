import os
import sys
import subprocess
import numpy as np 
import argparse 
from. import  _defaults 
from . import _ala_mut   

# general_method
# mmbpsa_in_gen


def input_args_check( input_arg_path = "tmp_input_file_salt") -> dict :
    cwd = os.getcwd()
    '''
    want option for default names, and dynamic naming: 
        -require dynamic naming if not provided all in paths

    wnat to have inputs for the leap.in fatures
    want mmbpsa input opitons (include step stuff) :
        inputs: 
        start_frame :
        end_frame
        interval : 

    '''
    input_fields={"WILD_TYPE": [], 
                "MUTATIONS":[],
                "*MDCRD_DIRECTORY": cwd, 
                "LEAP.IN_PATH" : [], 
                "MMPBSA.IN_PATH": [],
                "MMPBSA.SH_PATH": []
                }

    with open(input_arg_path, "r") as input_file:
        for line in input_file:
            if line.startswith("#input"):
                tmp_key = line.split() #split
                if tmp_key[2:] != [] : #check for null input 
                    input_fields[tmp_key[1]] = tmp_key[2:] #for args of len >1 e.g. MUTATIONS
    
    
    return input_fields



def input_args_from_text( file_handle ) -> list :
    with open(file_handle) as input_file :
        for line in input_file : 
            input_arg_list = []
    return input_arg_list 

def ala_main(input_dict,just_build ):
    pdbfh = input_dict["WILD_TYPE"][0]
    pdbfh_base_name = os.path.basename(pdbfh).split(".")[0] #getting the base name 
    print(input_dict["MUTATIONS"])
    ####################MMPBSA in file gen 

    _defaults.mmbpsa_in_gen(input_dict)
    for i in range(len(input_dict["MUTATIONS"])) : 
        mutation = input_dict["MUTATIONS"][i]
        _ala_mut.general_method(input_dict, pdbfh, pdbfh_base_name, mutation, just_build)

def main(args):
    
    in_file = args.input_file
    input_dict = input_args_check(in_file)
    just_build = args.just_build
    
    ala_main(input_dict,just_build)
    

    
if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description="High Throughput Mutational Analsys for MM/PB(GB)SA methods in Amber. The tool supports both Alanine and Non-Alanine scanning mutations. See dcoumentation for more details.")
    parser.add_argument("--input_file", type=str, help="Input file with the required parameters for the analysis. ")
    parser.add_argument(
        "--just_build",
        action="store_true", 
        default=False,      # The default value if the flag is not provided.
        help="If set, the .sh files for each run will be made but not run."
    )
    args= parser.parse_args()
    main(args)