import os
import sys
import subprocess
import numpy as np 
import argparse 
import glob
import shutil
from. import  _defaults 
from . import _ala_mut   
from . import _non_ala_mut
from . import _utils


def input_args_check( input_arg_path = "tmp_input_file.txt") -> dict :
    cwd = os.getcwd()
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

def ala_main(input_dict,just_build, amber_source ):
    pdbfh = input_dict["WILD_TYPE"][0]
    pdbfh_base_name = os.path.basename(pdbfh).split(".")[0] #getting the base name 
    print(input_dict["MUTATIONS"])
    #############MMPBSA in file gen 
    _defaults.mmbpsa_in_gen(input_dict)
    for i in range(len(input_dict["MUTATIONS"])) : 
        mutation = input_dict["MUTATIONS"][i]
        _ala_mut.general_method(input_dict, 
                                pdbfh, pdbfh_base_name,
                                mutation, just_build, amber_source)




def non_ala_main(input_dict, just_build, amber_source ):
    pdbfh_wild = input_dict["WILD_TYPE"][0]
    pdbfh_wild_base_name = os.path.basename(pdbfh_wild).split(".")[0]
    print(input_dict["MUTATIONS"])
    
    for mutation in input_dict["MUTATIONS"]:
        dir_str = "_" + mutation
        if not os.path.exists(dir_str):
            os.makedirs(dir_str)
            
        _non_ala_mut.general_mutate(modelname=pdbfh_wild_base_name, mutation=mutation)
        os.chdir(dir_str)
        pdb_file = f"{pdbfh_wild_base_name}{mutation}.pdb"
        subprocess.run(["move", pdb_file, dir_str], shell=True)
        _non_ala_mut.non_ala_file_pop(pdb_file, amber_source)
        os.chdir("..")
        #TODO update this 
        for in_file in glob.glob("gen_in_files\*.in"):
            shutil.copy(in_file, dir_str)

def main(args):
    in_file = args.input_file
    input_dict = input_args_check(in_file)
    just_build = args.just_build
    test_mode = args.test
    non_ala  = args.non_ala
    
    if args.amber_path is None:
        if test_mode:
            amber_source = "amber22/amber.sh"
        else:
            _utils.check_amber_loaded()
            amber_source = os.path.normpath(os.path.abspath(_utils.get_amber_home_path())) 
    else:
        amber_source = args.amber_path
    
    if non_ala:
        non_ala_main(input_dict, just_build, amber_source=amber_source )
    else:
        ala_main(input_dict,just_build, amber_source =amber_source)
    

    
if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description="High Throughput Mutational Analsys for MM/PB(GB)SA methods in Amber. The tool supports both Alanine and Non-Alanine scanning mutations. See dcoumentation for more details.")
    parser.add_argument("--input_file", type=str, help="Input file with the required parameters for the analysis. ")
    parser.add_argument(
        "--just_build",
        action="store_true", 
        default=False,     
        help="If set, the .sh files for each run will be made but not run."
    )
    parser.add_argument(
        "--amber_path",
        type=str,
        default=None, 
        help="Optional: Specify the full path to the AMBERHOME directory. If not provided, the script will attempt to use the AMBERHOME environment variable."
    )
    parser.add_argument(
        "--test",
        action="store_true", 
        default=False,      
        help="Optional: Run the script in test mode (e.g., for debugging or dry runs). This will use a fake amber path for users that just wish to test out the pipeline features on their local machines wihout needing Amber"
    )
    parser.add_argument(
        "--non_ala",
        action="store_true",  
        default=False,        
        help="Optional: Enable Non-Alanine scanning mutations. By default, Alanine scanning is assumed. Note you can still perform Alanine Mutations with this method, but it will force a modeller call. We suggest doing any Alanine scanning on its own, i.e. deploy the ala and non_ala pipelines."
    )
    args= parser.parse_args()
    main(args)