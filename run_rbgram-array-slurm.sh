#!/bin/bash

# shell script to submit array slurm jobs to run pipeline on full corpora directories. 
#   Calls 'sbatch /share/compling/projects/sanpi/slurm/bigram-array.slurm.sh'.
#
# The following can be passed to specify pattern directories (in ./Pat/) to pass to slurm script. If none is given, '--direct' will be used.
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
#
#  shortcuts to selecting subarrays:
#       --demo
#         array=35-37 (data/sanpi/subset/bigram_demo/*)
#       --debug
#         array=38-40 (data/sanpi/debug/bigram_debug/*)
#       --full
#         array=0-34 (data/sanpi/subsets/bigram_{news,puddin}/*)
# 
#  mode options are: "solo" for a single core/cpu and "multi" for multiple cpus requested (for parallel processing)
#
# usage: bash /share/compling/projects/sanpi/run_rbgram-array-slurm.sh [PAT_FLAG] [ARRAY_FLAG] [MODE]
# example: bash /share/compling/projects/sanpi/run_rbgram-array-slurm.sh multi --mirror --debug
# EVERYTHING: bash /share/compling/projects/sanpi/run_rbgram-array-slurm.sh multi --all_pat

HELP="shell script to submit array slurm jobs to run pipeline on full corpora directories. \n> \`sbatch /share/compling/projects/sanpi/slurm/bigram-array.slurm.sh\`.\n\nThe following can be passed to specify pattern directories (in ./Pat/) to pass to slurm script. If none is given, '--direct' will be used.\n\t--rbgrams\n\t\tBigram baseline, with ADV restricted to RB\n\t\tPATS=(\"RBXadj\")\n\t--neg\n\t\tall main negated patterns (set complement approach):\n\t\tPATS=(\"RBdirect\" \"RBscoped\" \"RBraised\")\n\t--direct\n\t\tnegated with *direct* dependency relation between NEG and ADJ nodes\n\t\tPATS=(\"RBdirect\")\n\t--indirect\n\t\tnegated with *indirect* dependency relation (1+ intervening node)\n\t\tPATS=(\"RBscoped\" \"RBraised\")\n\t--mirror\n\t\tPositive and Negative \"mirror\" patterns (explicit retrieval approach)\n\t\tPATS=(\"POSmirror\" \"NEGmirror\")\n\t--npi (added on a whim; *.pat not verified)\n\t\tPatterns for specific literature-identified NPIs\n\t\tPATS=(\"negpol\")\n\t[directory name]\n\t\tany (single) directory name in \"./Pat/\"\n  shortcuts to selecting subarrays:\n\t --demo\n\t\t array=35-37 (data/sanpi/subset/bigram_demo/*)\n\t --debug\n\t\t array=38-40 (data/sanpi/debug/bigram_debug/*)\n\t --full\n\t\t array=0-34 (data/sanpi/subsets/bigram_{news,puddin}/*)\n\nMODE options are: \"solo\" for a single core/cpu OR \"multi\" for multiple cpus requested (for parallel processing)\n\nusage:\n\tbash /share/compling/projects/sanpi/run_rbgram-array-slurm.sh [PAT_FLAG] [ARRAY_FLAG] [MODE]\nexample:\n\tbash /share/compling/projects/sanpi/run_rbgram-array-slurm.sh multi --mirror --debug\n-----------\nEVERYTHING:\n-----------\n\tbash /share/compling/projects/sanpi/run_rbgram-array-slurm.sh multi --all_pat"

CPUS=5
CPU_MEM=5G
MODE='multi'
echo "Running /share/compling/projects/sanpi/run_rbgram-array-slurm.sh"

#> Parse command-line arguments to customize job parameters
#   Exits with an error message for invalid options
while getopts ":p:m:a:h" opt; do
  case $opt in
    p) PAT_FLAG="${OPTARG}" ;;  # Store the Pat/dirname or flag
    m) MODE="${OPTARG}" ;;  # Store the mode value
    a) ARRAY_FLAG="${OPTARG}" ;;  # Store the number of corpus parts
    h) echo -e "${HELP}"; exit 0;;
    \?) echo "Invalid option -$OPTARG" >&2; exit 1 ;;
    esac
done

date
echo "PAT_FLAG: ${PAT_FLAG}"
echo "ARRAY_FLAG: ${ARRAY_FLAG}"
echo "MODE: ${MODE}"

LOG_DIR="/share/compling/projects/sanpi/logs/${ARRAY_FLAG//-}_bigram-pipeline_$(date +%y-%m-%d)"
mkdir -p ${LOG_DIR}

if [[ $(which grew && grew version) ]]; then
    date
    echo 'grew module found'

    #* Pattern selection based on PAT_FLAG
    if [[ ${PAT_FLAG} == '--rbgrams' ]]; then
        PATS=("RBXadj")

    elif [[ ${PAT_FLAG} == '--direct' ]]; then
        PATS=("RBdirect")

    elif [[ ${PAT_FLAG} == '--init' ]]; then
        PATS=("RBXadj" "RBdirect" "RBscoped" "RBraised")

    elif [[ ${PAT_FLAG} == '--main' ]]; then
        PATS=("RBXadj" "RBdirect" "RBscoped" "RBraised" "POSmirror" "NEGmirror")

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
    if [[ ${ARRAY_FLAG} == '--demo' ]]; then
        ARRAY_FLAG="--array=35-37"
    elif [[ ${ARRAY_FLAG} == '--debug' ]]; then
        ARRAY_FLAG="--array=38-40"
    elif [[ ${ARRAY_FLAG} == '--full' ]]; then
        ARRAY_FLAG="--array=0-34"
    fi

    echo -e "\nPatterns to submit jobs for: ${PATS[@]}"
    echo "Array Index of Corpus Parts to Search: ${ARRAY_FLAG#--array=}"
    
    #* Job submission based on MODE
    for PAT in "${PATS[@]}"; do
        echo -e "\n## $PAT\n"
        JOB_NAME="-J bigram-${PAT}_$(date +%y-%m-%d_%H%M)"
        if [[ ${MODE} == 'multi' ]]; then
            # echo 'sbatch ${JOB_NAME} ${ARRAY_FLAG} ./bigram-array.slurm.sh ${PAT}'
            echo -e "sbatch ${JOB_NAME}\n    ${ARRAY_FLAG}\n    --cpus-per-task ${CPUS} --mem-per-cpu=${CPU_MEM}\n    --chdir=${LOG_DIR} \n  bigram-array.slurm.sh ${PAT}"
            sbatch ${JOB_NAME} ${ARRAY_FLAG} --cpus-per-task ${CPUS} --mem-per-cpu=${CPU_MEM} --chdir=${LOG_DIR} /share/compling/projects/sanpi/slurm/bigram-array.slurm.sh ${PAT}

        elif [[ ${MODE} == 'solo' ]]; then
            echo -e "sbatch ${JOB_NAME} ${ARRAY_FLAG} -n 1 --mem=15G\n    --chdir=${LOG_DIR} bigram-array.slurm.sh ${PAT}"
            sbatch ${JOB_NAME} ${ARRAY_FLAG} -n 1 --mem=15G --chdir=${LOG_DIR} /share/compling/projects/sanpi/slurm/bigram-array.slurm.sh ${PAT}
        else
            echo -e "No valid cpu mode given. First argument should be one of the following strings:\n+ 'solo' for 1 core/cpu\n~or~\n+ 'multi' for multiple cores/cpus"
        fi

    done
else
    echo -e 'grew installation not found. Check conda environment.\n** If running in screen, make sure calling env has access to grew as well.'
fi
