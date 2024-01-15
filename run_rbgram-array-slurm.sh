#!/bin/bash

# shell script to submit array slurm jobs to run pipeline on full corpora directories. Calls 'sbatch /share/compling/projects/sanpi/slurm/bigram-array.slurm.sh'.
#
#  1 of the following can be passed to specify pattern directories to run (directories in ./Pat/) If none is given, '--direct' will be used.
#      --rbgrams
#        Bigram baseline, with ADV restricted to RB
#          PATS=("RBXadj")
#      --neg
#        all main negated patterns (set complement approach):
#          PATS=("RBdirect" "RBscoped" "RBraised")
#      --direct
#        negated with *direct* dependency relation between NEG and ADJ nodes
#          PATS=("RBdirect")
#      --indirect
#        negated with *indirect* dependency relation (1+ intervening node)
#          PATS=("RBscoped" "RBraised")
#      --mirror
#        Positive and Negative "mirror" patterns (explicit retrieval approach)
#          PATS=("POSmirror" "NEGmirror")
#      --npi (added on a whim; *.pat not verified)
#        Patterns for specific literature-identified NPIs
#          PATS=("negpol")
#      [directory name]
#          any (single) directory name in "./Pat/"

# example: bash /share/compling/projects/sanpi/run_bigram-array-slurm.sh multi --mirror --debug
# EVERYTHING: bash /share/compling/projects/sanpi/run_bigram-array-slurm.sh multi --all_pat

CPUS=10
CPU_MEM=5G

echo "Running /share/compling/projects/sanpi/run_bigram-array-slurm.sh"
date
LOG_DIR=/share/compling/projects/sanpi/logs/bigram-pipeline_$(date "+%y-%m-%d")
mkdir -p ${LOG_DIR}
MODE=$1
PAT_FLAG=${2:-""}
echo "PAT_FLAG: ${PAT_FLAG}"
ARRAY_FLAG=${3:-""}
echo "ARRAY_FLAG: ${ARRAY_FLAG}"


if [[ $(which grew && grew version) ]]; then
    date
    echo 'grew module found'

    if [[ ${PAT_FLAG} == '--rbgrams' ]]; then
        PATS=("RBXadj")

    elif [[ ${PAT_FLAG} == '--direct' ]]; then
        PATS=("RBdirect")

    elif [[ ${PAT_FLAG} == '--neg' ]]; then
        PATS=("RBdirect" "RBscoped" "RBraised")

    elif [[ ${PAT_FLAG} == '--mirror' ]]; then
        PATS=("POSmirror" "NEGmirror")

    elif [[ ${PAT_FLAG} == '--noncontig' ]]; then
        PATS=("RBscoped" "RBraised")

    elif [[ ${PAT_FLAG} == '--npi' ]]; then
        PATS=("negpol")

    elif [[ -d "/share/compling/projects/sanpi/Pat/${PAT_FLAG}" ]]; then
        PATS=("${PAT_FLAG}")

    else
        PATS=("RBdirect")
    fi
    echo
    if [[ ${ARRAY_FLAG} == '--debug' ]]; then
        ARRAY_FLAG="--array=35-37"
    elif [[ ${ARRAY_FLAG} == '--full' ]]; then
        ARRAY_FLAG="--array=0-34"
    fi
    
    echo -e "\nPatterns to submit jobs for: ${PATS[@]}"
    echo "Array Index of Corpus Parts to Search: ${ARRAY_FLAG#--array=}"
    for PAT in "${PATS[@]}"; do
        echo -e "\n## $PAT\n"
        JOB_NAME="-J bigram-${PAT}_$(date +%y-%m-%d_%H%M)"
        if [[ ${MODE} == 'multi' ]]; then
            # echo 'sbatch ${JOB_NAME} ${ARRAY_FLAG} ./bigram-array.slurm.sh ${PAT}'
            echo "sbatch ${JOB_NAME} ${ARRAY_FLAG} --cpus-per-task ${CPUS} --mem-per-cpu=${CPU_MEM} --chdir=${LOG_DIR} bigram-array.slurm.sh ${PAT}"
            # exit #! #HACK temp exit >> remove
            sbatch ${JOB_NAME} ${ARRAY_FLAG} --cpus-per-task ${CPUS} --mem-per-cpu=${CPU_MEM} --chdir=${LOG_DIR} /share/compling/projects/sanpi/slurm/bigram-array.slurm.sh ${PAT}

        elif [[ ${MODE} == 'solo' ]]; then
            # echo 'sbatch ${JOB_NAME} ${ARRAY_FLAG} ./bigram-array.slurm.sh ${PAT}'
            echo "sbatch ${JOB_NAME} ${ARRAY_FLAG} -n 1 --mem=15G --chdir=${LOG_DIR} bigram-array.slurm.sh ${PAT}"
            sbatch ${JOB_NAME} ${ARRAY_FLAG} -n 1 --mem=15G --chdir=${LOG_DIR}  /share/compling/projects/sanpi/slurm/bigram-array.slurm.sh ${PAT}
        else
            echo -e  "No valid cpu mode given. First argument should be one of the following strings:\n+ 'solo' for 1 core/cpu\n~or~\n+ 'multi' for multiple cores/cpus"
        fi

    done
else
    echo -e 'grew installation not found. Check conda environment.\n** If running in screen, make sure calling env has access to grew as well.'
fi
