#!/bin/bash
##SBATCH --mail-user=arh234@cornell.edu
##SBATCH --mail-type=ALL
#SBATCH -J subset                 # Job name
#SBATCH -o %x_%j.out              # Name of stdout output log file (%j expands to jobID)
#SBATCH -e %x_%j.err              # Name of stderr output log file (%j expands to jobID)
##SBATCH --open-mode=append
#SBATCH --nodes=1                       # Total number of nodes requested
#SBATCH --ntasks=1                      # Total number of tasks (defaults to 1 cpu/task, but overrride with -c)
#SBATCH --cpus-per-task=10              # number of cpus per task
##SBATCH --ntasks-per-socket=1
#SBATCH --mem-per-cpu=8G               # Total amount of (real) memory requested (per node)
#SBATCH --time 48:00:00                  # Time limit (hh:mm:ss)
#SBATCH --get-user-env
#SBATCH --chdir=/share/compling/data/sanpi/logs/subsets    # change cwd before execution

echo "RUNNING solo_dir_subset_slurm.sh"
date "+%F %X"
SOURCE_DIR=/share/compling/projects/sanpi
#> $1 = .conll/ dir path (absolute)
#> $2 = .pat file path (absolute)
#* conll dir is required but pat can default to advadj
PAT=${2:-}
python ${SOURCE_DIR}/script/make_subset.sh $1 $PAT
