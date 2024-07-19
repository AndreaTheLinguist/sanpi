#!/bin/bash
#SBATCH -N1
#SBATCH -n1
#SBATCH --mem=88G
#SBATCH -o %x.%j.out
#SBATCH -e %x.%j.err
#SBATCH --time 12:00:00
#SBATCH -J count_RBgrams
#SBATCH --requeue
#SBATCH --chdir=/share/compling/projects/sanpi/logs/count_RBgrams

# usage:    sbatch [slurm flags] count_RBgrams.slurm.sh [-f N_FILES] [-t THRESH] [-d DATA_DIR_NAME]
# usage:    sbatch [slurm flags] count_RBgrams.slurm.sh -f '-f 3' -t '-t 0.001' -d '/share/compling/data/sanpi/debug/2_hit_tables/RBXadj'
SANPI_DATA="/share/compling/data/sanpi"
RESULTS="/share/compling/projects/sanpi/results"

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
THRESH=''
HIT_DATA_DIR="${SANPI_DATA}/${REL_HIT_DIR}"
DIR_N_FILES="$(ls -d1 ${HIT_DATA_DIR}/*pkl.gz | wc -l)"
N_FILES="${DIR_N_FILES% }"
# Parse command-line arguments to customize job parameters
while getopts ":t:f:d:" opt; do
  case $opt in
    t) THRESH="${OPTARG/\%/}" ;;  # Store the threshold percentage
    f) N_FILES="${OPTARG%f}" ;;  # Store the number of corpus parts
    d) HIT_DATA_DIR="${OPTARG}" ;;  
    \?) echo "Invalid option -$OPTARG" >&2; exit 1 ;;
    esac
done


if [[ -n $THRESH ]]; then
    THRESH="-t ${THRESH/#* }"
fi

if [[ $HIT_DATA_DIR == "demo" ]]; then
    HIT_DATA_DIR="${SANPI_DATA}/DEMO/${REL_HIT_DIR}"
    #> update number of files in dir

    DIR_N_FILES="$(ls -d1 ${HIT_DATA_DIR}/*pkl.gz | wc -l)"
    #> replace "results" with "DEMO/results"
    RESULTS="${RESULTS/results/'DEMO/results'}"
fi

N_FILES=${N_FILES// /}
if (( ${N_FILES} > ${DIR_N_FILES% } )); then
    N_FILES=${DIR_N_FILES// /}
fi

N_FILES=${N_FILES:+"-f ${N_FILES}"}

mkdir -p $RESULTS

DATA_DIR_NAME=$(basename ${HIT_DATA_DIR})
echo "processing ➡️ ${HIT_DATA_DIR//*data/..}"
POST_PROC_DIR="${HIT_DATA_DIR%2_hit_tables*}4_post-processed/${DATA_DIR_NAME}"
PROG="/share/compling/projects/sanpi/source/analyze/count_bigrams.py -p ${POST_PROC_DIR} -o ${RESULTS}/freq_out/${DATA_DIR_NAME}"
# usage: count_bigrams.py [-h] [-f N_FILES] [-t PERCENT_HITS_THRESHOLD] [-d DATA_DIR] [-p POST_PROC_DIR] [-o FRQ_OUT_DIR] [-g FRQ_GROUPS] [-s]
# echo 'time python $PROG $N_FILES $THRESH -d $HIT_DATA_DIR'
echo "time python $PROG $N_FILES $THRESH -d $HIT_DATA_DIR"
time python $PROG $N_FILES $THRESH -d $HIT_DATA_DIR 
#// >> >(tee -i -a ${LOG_FILE}) 2>&1