#!/bin/bash

# shell script to submit array slurm jobs to run pipeline on full corpora directories. Calls 'sbatch /share/compling/projects/sanpi/sanpi-array.slurm.sh'.
#
#  1 of the following can be passed to specify pattern directories to run (directories in ./Pat/) If none is given, '--neg' will be used.
#
#      --all_pat
#          all main patterns:
#              'PATS=("contig" "scoped" "raised" "advadj")'
#
#      --neg
#          all main negated patterns:
#              'PATS=("contig" "scoped" "raised" "advadj")'
#
#      --noncontig
#          main negated patterns excluding 'contig':
#              'PATS=("scoped" "raised")'
#
#      [directory name]
#          any (single) directory name in "./Pat/"

# (which grew && grew version) && (date; echo 'pats=("contig" "scoped" "raised" "advadj");for pat in "${pats[@]}"; do sbatch -J ${pat}DEMO exactly-array.demo-slurm.sh ${pat}; done'; pats=("contig" "scoped" "raised" "advadj"); for pat in "${pats[@]}"; do echo "# ${pat}"; echo "sbatch -J ${pat}DEMO exactly-array.demo-slurm.sh ${pat}"; sbatch -J ${pat}DEMO exactly-array.demo-slurm.sh ${pat}; done)

echo "Running /share/compling/projects/sanpi/run_sanpi-array-slurm.sh"

MODE=$1
PAT_FLAG=${2:-"--neg"}
echo "PAT_FLAG: $PAT_FLAG"
ARRAY=${3:-""}
echo "ARRAY: $ARRAY"

if [[ $(which grew && grew version) ]]; then
    date
    echo 'grew module found'
    if [[ $PAT_FLAG == '--all_pat' ]]; then
        PATS=("contig" "scoped" "raised" "advadj")

    elif [[ $PAT_FLAG == '--neg' ]]; then
        PATS=("contig" "scoped" "raised" "advadj")

    elif [[ $PAT_FLAG == '--noncontig' ]]; then
        PATS=("scoped" "raised")

    elif [[ -d "Pat/$PAT_FLAG" ]]; then
        PATS=("$PAT_FLAG")

    else
        PATS=("contig")
        ARRAY=$PAT_FLAG
        echo "(update) ARRAY = $ARRAY"

    fi

    echo -e "\nPatterns to submit jobs for: ${PATS[@]}"
    for PAT in "${PATS[@]}"; do

        echo -e "\n# $PAT"

        if [[ $MODE == 'multi' ]]; then
            # echo 'sbatch -J $PAT $ARRAY ./sanpi-array.slurm.sh $PAT'
            echo "sbatch -J $PAT $ARRAY ./sanpi-array.slurm.sh $PAT"
            sbatch -J $PAT $ARRAY -n 12 --mem-per-cpu=14G /share/compling/projects/sanpi/sanpi-array.slurm.sh $PAT

        elif [[ $MODE == 'solo' ]]; then
            # echo 'sbatch -J $PAT $ARRAY ./sanpi-array.slurm.sh $PAT'
            echo "sbatch -J $PAT $ARRAY ./sanpi-array.slurm.sh $PAT"
            sbatch -J $PAT $ARRAY -n 1 --mem=10G /share/compling/projects/sanpi/sanpi-array.slurm.sh $PAT
        else
            echo -e  "No valid cpu mode given. First argument should be one of the following strings:\n+ 'solo' for 1 core/cpu\n~or~\n+ 'multi' for multiple cores/cpus"
        fi

    done
else
    echo -e 'grew installation not found. Check conda environment.\n** If running in screen, make sure calling env has access to grew as well.'
fi
