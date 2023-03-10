#!/bin/bash
'''shell script to submit array slurm jobs to run pipeline on full corpora directories. Calls 'sbatch /share/compling/projects/sanpi/sanpi-array.slurm.sh'. 

    1 of the following can be passed to specify pattern directories to run (directories in ./Pat/) If none is given, '--neg' will be used.

    --all_pat
        all main patterns: 
          'PATS=("contig" "scoped" "raised" "advadj")'

    --neg
        all main negated patterns: 
          'PATS=("contig" "scoped" "raised" "advadj")'

    --noncontig
        main negated patterns excluding 'contig': 
          'PATS=("scoped" "raised")'

    [directory name]
        any (single) directory name in "./Pat/"
'''
#/share/compling/projects/sanpi/sanpi-array.slurm.sh

# (which grew && grew version) && (date; echo 'pats=("contig" "scoped" "raised" "advadj");for pat in "${pats[@]}"; do sbatch -J ${pat}DEMO exactly-array.demo-slurm.sh ${pat}; done'; pats=("contig" "scoped" "raised" "advadj"); for pat in "${pats[@]}"; do echo "# ${pat}"; echo "sbatch -J ${pat}DEMO exactly-array.demo-slurm.sh ${pat}"; sbatch -J ${pat}DEMO exactly-array.demo-slurm.sh ${pat}; done)
PAT_FLAG = ${1:-"--neg"}

if [[ `which grew && grew version` ]]; then
    date
    echo 'grew module found'
    if [[ ${PAT_FLAG} == '--all_pat' ]]; then
        PATS=("contig" "scoped" "raised" "advadj")

    elif [[ ${PAT_FLAG} == '--neg']]; then
        PATS=("contig" "scoped" "raised" "advadj")

    elif [[ ${PAT_FLAG} == '--noncontig']]; then
        PATS=("scoped" "raised")

    else
        PATS=("${PAT_FLAG}")
    fi

    echo "Pattern jobs to run: ${PATS[@]}"
    for PAT in "${PATS[@]}"; do 
        echo -e "\n# ${PAT}"
        echo "sbatch -J ${PAT} exactly-array.slurm.sh ${PAT}"
        sbatch -J ${PAT} /share/compling/projects/sanpi/sanpi-array.slurm.sh ${PAT};
    done
else
    echo -e 'grew installation not found. Check conda environment.\n** If running in screen, make sure calling env has access to grew as well.'    
fi
