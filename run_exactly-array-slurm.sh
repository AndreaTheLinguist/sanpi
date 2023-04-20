#!/bin/bash

#/share/compling/projects/sanpi/slurm/exactly-array.slurm.sh

# (which grew && grew version) && (date; echo 'pats=("contig" "scoped" "raised" "advadj");for pat in "${pats[@]}"; do sbatch -J ${pat}DEMO exactly-array.demo-slurm.sh ${pat}; done'; pats=("contig" "scoped" "raised" "advadj"); for pat in "${pats[@]}"; do echo "# ${pat}"; echo "sbatch -J ${pat}DEMO exactly-array.demo-slurm.sh ${pat}"; sbatch -J ${pat}DEMO exactly-array.demo-slurm.sh ${pat}; done)

if [[ `which grew && grew version` ]]; then
    date
    echo 'grew module found'
    if [[ $1 == '--all_pat' ]]; then
        pats=("contig" "scoped" "raised" "advadj")
    else
        pats=("contig" "scoped" "raised")
    fi

    echo "Pattern jobs to run: ${pats[@]}"
    for pat in "${pats[@]}"; do 
        echo -e "\n# ${pat}"
        echo "sbatch -J ${pat} exactly-array.slurm.sh ${pat}"
        sbatch -J ${pat} /share/compling/projects/sanpi/slurm/exactly-array.slurm.sh ${pat};
    done
else
    echo -e 'grew installation not found. Check conda environment.\n** If running in screen, make sure calling env has access to grew as well.'    
fi
