#!/bin/bash
#SBATCH --job-name=run_equil
#SBATCH --partition=gpu
#SBATCH --gpus=4
#SBATCH --cpus-per-gpu=12
#SBATCH --output=run_equil.out
#SBATCH --error=run_equil.error
#SBATCH --time=48:00:00


# Check if AMBER source path is provided
if [ -z "$1" ]; then
    echo "Usage: $0 <path_to_amber_source.sh>"
    exit 1
fi

AMBER_SOURCE_PATH=$1

echo "Loading modules..."
module load amber
source "$AMBER_SOURCE_PATH"

$AMBERHOME/bin/pmemd.cuda -O -i min.in -o min.out -p 6m0j_noHet_solvated.prmtop -c 6m0j_noHet_solvated.inpcrd \
-r min.rst -ref 0.15_80_10_pH6.5_6m0j.BOX.inpcrd
echo "min done"
$AMBERHOME/bin/pmemd.cuda -O -i heat.in -o heat.out -p 6m0j_noHet_solvated.prmtop -c min.rst \
-r heat.rst -x heat.mdcrd -ref min.rst

echo "heat done"
$AMBERHOME/bin/pmemd.cuda -O -i density.in -o density.out -p 6m0j_noHet_solvated.BOX.prmtop -c heat.rst \
-r density.rst -x density.mdcrd -ref heat.rst


echo "density done"
$AMBERHOME/bin/pmemd.cuda -O -i equil.in -o equil.out -p 6m0j_noHet_solvated.prmtop -c density.rst \
-r equil.rst -x equil.mdcrd



