#!/bin/bash

# This script is used to customize and submit a slurm job for counting RBgrams. 
# Parses command-line arguments to set the threshold percentage, memory value, and number of corpus parts; 
# validates the threshold percentage, then displays the job specifications and submits the job using sbatch.
#
# Example usage: 
# bash /share/compling/projects/sanpi/run_count-RBgrams-slurm.sh -t 0.05 -m 16g -f 20

eval "$(conda shell.bash hook)"
conda activate sanpi
# default values
T=0005
M=97
F=35
DATA_FLAG=""

# Parse command-line arguments to customize job parameters
while getopts ":t:m:f:d:" opt; do
  case $opt in
    t) T="${OPTARG/\%/}" ;;  # Store the threshold percentage
    m) M="${OPTARG/g/}" ;;  # Store the memory value
    f) F="${OPTARG/f/}" ;;  # Store the number of corpus parts
    d) DATA_FLAG="-d ${OPTARG}" ;;  # Store the data dir as flag if given
    \?) echo "Invalid option -$OPTARG" >&2; exit 1 ;;
    esac
done

# Validate and format the threshold percentage
# Raises: Exits with an error message if the threshold is invalid
if [[ ! "${T}" =~ [0-1]*\.[0-1]+ ]]; then

    if [[ "${T}" =~ [a-zA-Z] ]]; then
        echo "Threshold percentange paramenter must be numerical: ([0-9].)[0-9]"
        exit 1
    elif [[ ${T::1} == '0' ]]; then 
        # assume first digit provided is tens place, prepend '.'
        T=".${T}"
        echo "Assuming decimal --> ${T}"
    elif (( $T > 4 )); then
        echo "ERROR: ${T}% threshold is too high! Did you forget a decimal or zeros?"
        exit 1
    fi 
fi

# Add leading zero if necessary
if [[ ${T::1} == '.' ]]; then
    echo '(added initial 0)'
    T="0${T}"
fi

T_LABEL="${T/./-}"
MEM="${M}g"

if [[ ${DATA_FLAG} =~ "demo" ]]; then
    LOG_DIR="/share/compling/projects/sanpi/DEMO/logs/count_RBgrams"
    mkdir -p ${LOG_DIR}
    LOG_DIR_FLAG=" --chdir=${LOG_DIR}"
    M="3"
    MEM="${M}g"
    if [[ ${F} == '35' ]]; then
        J="DEMO_${MEM}All~${T_LABEL}-RBgrams_$(date +%y-%m-%d)"
    fi
else
    J="${MEM}${F}f~${T_LABEL}-RBgrams_$(date +%y-%m-%d)"    
fi

DATA_ROW=${DATA_FLAG:+"\ndata flag/directory, ${DATA_FLAG#-d }"}

# Display job specifications and submit the job
echo -e "frequency threshold,${T}(%),\"${T_LABEL}\"\nmemory request,${M}(GB),\"${MEM}\"\ncorpus parts included,${F},\"${F}f\"${DATA_ROW}" | tabulate -s, -f 'rst'

MEM_FLAG="--mem=${M/G/}G"
JOB_FLAG="-J ${J}"
SH_PATH="/share/compling/projects/sanpi/slurm/count_RBgrams.slurm.sh"
REL_SH_PATH="${SH_PATH##$(pwd)/}"
SLURM_FLAGS="${MEM_FLAG} ${JOB_FLAG}${LOG_DIR_FLAG:-""}"
SH_ARGS="-f ${F} -t ${T}${DATA_FLAG:-""}"

echo -e ",Job Specs\ndate,$(date)\nslurm memory,${MEM_FLAG}\nslurm job name,${JOB_FLAG}\nscript, ${REL_SH_PATH}\narguments,\`${SH_ARGS}\`" | tabulate -s, -f "fancy_grid"
echo

echo "$(pwd)\$ sbatch ${SLURM_FLAGS} ${REL_SH_PATH} ${SH_ARGS}"

# ${SH_PATH} ${SH_ARGS} #HACK

sbatch ${SLURM_FLAGS} ${SH_PATH} ${SH_ARGS}