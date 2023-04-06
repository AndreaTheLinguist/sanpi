#!/bin/bash

date
echo ">>> subsets for patterns in: ${1}"
ls $1*pat | parallel ls {} STEM={/.}\; echo \$STEM \; TAG=\$\{STEM\%-*\}\; echo \$TAG\; echo "sbatch -J\$TAG-subset filter_subset_slurm.sh \$TAG {}"\; #sbatch -J\$TAG-subset filter_subset_slurm.sh \$TAG {}\; echo "---"
