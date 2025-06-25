import os
import sys
import subprocess
import numpy as np 

















def tleap_gen(pdbfh_base_name,file_handle_mut_all ) -> list:
    '''
    pdbfh_base_name     : base name of the pdb file
    file_handle_mut_all : base bame of the mutated file 
    returns             : tleap file as a list 
    '''

    tleap_wild_in = [f"source leaprc.protein.ff19SB",
        f"source leaprc.water.opc",
        f"set default PBRadii mbondi2\n",
        f"com = loadpdb {pdbfh_base_name}.pdb"  ,
        f"ligand = loadpdb {pdbfh_base_name}_ligand.pdb" ,
        f"rcp = loadpdb {pdbfh_base_name}_recpt.pdb\n",
        f"saveamberparm com {pdbfh_base_name}.prmtop {pdbfh_base_name}.inpcrd",
        f"saveamberparm ligand {pdbfh_base_name}_ligand.prmtop {pdbfh_base_name}_ligand.inpcrd",
        f"saveamberparm rcp {pdbfh_base_name}_recpt.prmtop {pdbfh_base_name}_recpt.inpcrd",
        f"solvatebox com TIP3PBOX 12.0",
        f"saveamberparm com {pdbfh_base_name}_solvated.prmtop {pdbfh_base_name}_solvated.inpcrd\n",
        f"com_mut = loadpdb {file_handle_mut_all}.pdb",
        f"ligand_mut = loadpdb {file_handle_mut_all}_ligand.pdb\n",
        f"saveamberparm com_mut {file_handle_mut_all}.prmtop {file_handle_mut_all}.inpcrd",
        f"saveamberparm ligand_mut {file_handle_mut_all}_ligand.prmtop {file_handle_mut_all}_ligand.inpcrd",
        f"quit"]
    return tleap_wild_in

#TODO fix source path 
def mut_bash( pdbfh_base_name, 
             file_handle_mut_all, 
             cwd, 
             amber_source,
             tleap_file_name : str ='tleap_mut.in') -> list:
    '''
    pdbfh_base_name     : base name of the pdb file
    file_handle_mut_all : base bame of the mutated file 
    cwd                 : cwd where script was called, this is parent dir afer chdir call
    returns             : .sh file as a list 
    '''
    
    mut_bash_sh = [f"#!/bin/bash",
        f"#SBATCH --job-name=run_{pdbfh_base_name}_mut",
        f"#SBATCH --partition=cpu",
        f"#SBATCH --ntasks=4",
        f"#SBATCH --cpus-per-task=1",
        f"#SBATCH --mem=10000",
        f"#SBATCH --output=run_mmpbsa_{pdbfh_base_name}.out",
        f"#SBATCH --error=run_mmpbsa_{pdbfh_base_name}.error",
        f"#SBATCH --time=72:00:00",
        f'''echo "Loading modules..."'''  ,  
        f"module load amber " ,
        f"source {amber_source}",
        f"",
        f"tleap -s -f {tleap_file_name} > tleap_mut.out"
        f"",
        f"""$AMBERHOME/bin/MMPBSA.py -O -i \
{cwd}/mmpbsa.in -o \
FINAL_RESULTS_MMPBSA_tleap_{file_handle_mut_all}.dat\
 -sp {pdbfh_base_name}_solvated.prmtop\
 -cp {pdbfh_base_name}.prmtop\
 -rp {pdbfh_base_name}_recpt.prmtop\
 -lp {pdbfh_base_name}_ligand.prmtop\
 -y {cwd}/*.mdcrd\
 -mc {file_handle_mut_all}.prmtop\
 -ml {file_handle_mut_all}_ligand.prmtop"""
        ]
    return mut_bash_sh

    # f"{cwd}/change_radii_to_opt.py {pdbfh_base_name}_solvated.prmtop",
    #     f"{cwd}/change_radii_to_opt.py {pdbfh_base_name}.prmtop",
    #     f"{cwd}/change_radii_to_opt.py {pdbfh_base_name}_ligand.prmtop",
    #     f"{cwd}/change_radii_to_opt.py {file_handle_mut_all}.prmtop", 
    #     f"{cwd}/change_radii_to_opt.py {file_handle_mut_all}_ligand.prmtop",
    #     f"{cwd}/change_radii_to_opt.py {pdbfh_base_name}_recpt.prmtop",

def mmpbsa_in()->list:
    mmpbsa_in_data = [
f"""
sample input file for running alanine scanning
 &general
   startframe=1, endframe=2000, interval=5, 
   verbose=1
/
&gb
  igb=66, saltcon=0.145
/
&pb
    istrng=0.145,
/
&alanine_scanning
/
"""] 
    return mmpbsa_in_data