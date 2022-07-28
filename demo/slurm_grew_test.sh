#!/bin/bash
#SBATCH -N1 
#SBATCH -n3 
##SBATCH --mem=40G
#SBATCH --mem-per-cpu=15G 
#SBATCH --partition=compling
#SBATCH -o mp-test-sub20_%j.out
#SBATCH -e mp-test-sub20_%j.err
#SBATCH --time 1:30:00
#SBATCH -J testing-pool-runs
#SBATCH --chdir=/share/compling/projects/sanpi/demo


eval "$(conda shell.bash hook)"
conda activate sanpi
DEMO_DIR=/share/compling/projects/sanpi/demo
python ${DEMO_DIR}/source/gather/grew_search.py ${DEMO_DIR}/data/corpora/puddin/x20_subset_exactly ${DEMO_DIR}/Pat/filter/exactly-JJ.pat ${DEMO_DIR}/data/1_json_grew-matches