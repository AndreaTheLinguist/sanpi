#! /bin/bash

LOG="logs/make-ucs-tsv/FINAL-direct_freq-tsvs_$(date +%y-%m-%d_%I%P).log"
echo -e "Log set to\n-> '${LOG}'"
touch "${LOG}" || exit

echo '>>> "ALL*RBdirect"'
(
    echo '>>> "ALL*RBdirect"'
    bash script/cat_tsvs.sh || exit
) >"${LOG}" 2>&1 

echo '>>> "NEQ*RBdirect"'
(
    echo -e '=====================\n>>> "NEQ*RBdirect"\n'
    bash script/cat_tsvs.sh -s || exit
) >>"${LOG}" 2>&1

LOG="${LOG/direct/mirror}"
echo -e "Log set to\n-> '${LOG}'"
touch "${LOG}" || exit

echo '>>> "ALL*mirror"'
(
    echo '>>> "ALL*mirror"'
    bash script/cat_tsvs.sh -p mirror || exit
) >"${LOG}" 2>&1

echo '>>> "NEQ*mirror"'
(
    echo -e '=====================\n>>> "NEQ*mirror"\n'
    bash script/cat_tsvs.sh -p mirror -s || exit
) >>"${LOG}" 2>&1
