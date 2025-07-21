import os
import sys
import subprocess
import numpy as np 
import argparse 
from _defaults import tleap_gen, mut_bash, mmpbsa_in 





def input_args_check( input_arg_path) -> dict :
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

    with open("tmp_input_file_salt.txt", "r") as input_file:
        for line in input_file:
            if line.startswith("#input"):
                tmp_key = line.split() #split
                if tmp_key[2:] != [] : #check for null input 
                    input_fields[tmp_key[1]] = tmp_key[2:] #for args of len >1 e.g. MUTATIONS
    
    
    return input_fields




def input_args_from_text( file_handle ) -> list :
    with open(file_handle) as input_file :
        for line in input_file : 
            input_arg_list = [] #add real input here
    return input_arg_list 

def main(args):
    
    in_file = args.input_file
    input_dict = input_args_check(in_file)
    
    pdbfh = input_dict["WILD_TYPE"][0]
    pdbfh_base_name = os.path.basename(pdbfh).split(".")[0] #getting the base name 
    print(input_dict["MUTATIONS"])
    #MMPBSA in file gen 

    mmbpsa_in_gen(input_dict)
    for i in range(len(input_dict["MUTATIONS"])) : 
        mutation = input_dict["MUTATIONS"][i]
        general_method(input_dict, pdbfh, pdbfh_base_name, mutation)


    ##TODO add creations of summary file: 
    
if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description="High Throughput Mutational Analsys for MM/PB(GB)SA methods in Amber. The tool supports both Alanine and Non-Alanine scanning mutations. See dcoumentation for more details.")
    parser.add_argument("--input_file", type=str, help="Input file with the required parameters for the analysis. ")
    args= parser.parse_args()
    main(args)