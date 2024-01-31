#!/bin/bash
#SBATCH -N1
#SBATCH -n1
#SBATCH --mem=50G
#SBATCH -o %x.%j.out
#SBATCH -e %x.%j.err
#SBATCH --time 12:00:00
#SBATCH -J count_RBgrams
#SBATCH --requeue
#SBATCH --chdir=/share/compling/projects/sanpi/logs/count_RBgrams

# usage:    sbatch [slurm flags] count_RBgrams.slurm.sh [N_FILES] [THRESH] [DATA_DIR_NAME]
# usage:    sbatch [slurm flags] count_RBgrams.slurm.sh '-f 3' '-t 0.001' '/share/compling/data/sanpi/debug/2_hit_tables/RBXadj'
SANPI_DATA="/share/compling/data/sanpi"

echo 'running slurm script: /share/compling/projects/sanpi/slurm/count_RBgrams.slurm.sh'
echo "JOB ID: ${SLURM_JOB_ID}"
echo "JOB NAME: ${SLURM_JOB_NAME}"
echo "started @ $(date '+%F %X') from $(pwd)"
echo ". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . ."
echo "running on ${SLURM_JOB_NODELIST} with `nproc` cores"
echo "* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *"

eval "$(conda shell.bash hook)"
conda activate sanpi
REL_HIT_DIR="2_hit_tables/RBXadj"
HIT_DATA_DIR=${1:-"${SANPI_DATA}/${REL_HIT_DIR}"}
RESULTS="/share/compling/projects/sanpi/results"

if [[ $HIT_DATA_DIR == "--demo" ]]; then
    HIT_DATA_DIR="${SANPI_DATA}/DEMO/${REL_HIT_DIR}"
    #> replace "results" with "DEMO/results"
    RESULTS="${RESULTS/results/DEMO/results}"
fi

mkdir -p $RESULTS

N_FILES=${2:-"$(ls -d1 ${HIT_DATA_DIR}/*pkl.gz | wc -l)"}
N_FILES="-f ${N_FILES/#* }"
THRESH=${3:-''}
if [[ -n $THRESH ]]; then
    THRESH="-t ${THRESH/#* }"
fi

DATA_DIR_NAME=$(basename ${HIT_DATA_DIR})
echo "processing ➡️ ${HIT_DATA_DIR//*data/..}"
POST_PROC_DIR="${HIT_DATA_DIR%2_hit_tables*}4_post-processed/${DATA_DIR_NAME}"
PROG="/share/compling/projects/sanpi/source/analyze/count_bigrams.py -p ${POST_PROC_DIR} -o ${RESULTS}/freq_out/${DATA_DIR_NAME}"

echo 'time python $PROG $N_FILES $THRESH -d $HIT_DATA_DIR'
echo "time python $PROG $N_FILES $THRESH -d $HIT_DATA_DIR"
time python $PROG $N_FILES $THRESH -d $HIT_DATA_DIR #>> >(tee -i -a ${LOG_FILE}) 2>&1