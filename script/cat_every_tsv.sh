#! /bin/bash

LOG="logs/make-ucs-tsv/FINAL-direct_freq-tsvs_$(sday_h12).log"
echo -e "Log set to\n-> '${LOG}'"
touch "${LOG}" &&
    echo '>>> "ALL*RBdirect"'
(
    echo '>>> "ALL*RBdirect"'
    bash script/cat_tsvs.sh
) >"${LOG}" 2>&1 &&
    echo '>>> "NEQ*RBdirect"'
(
    echo -e '=====================\n>>> "NEQ*RBdirect"\n'
    bash script/cat_tsvs.sh -s
) >>"${LOG}" 2>&1 &&
    LOG="${LOG/direct/mirror}"
echo -e "Log set to\n-> '${LOG}'"
touch "${LOG}" &&
    echo '>>> "ALL*mirror"'
(
    echo '>>> "ALL*mirror"'
    bash script/cat_tsvs.sh -p mirror
) >"${LOG}" 2>&1 &&
    echo '>>> "NEQ*mirror"'
(
    echo -e '=====================\n>>> "NEQ*mirror"\n'
    bash script/cat_tsvs.sh -p mirror -s
) >>"${LOG}" 2>&1
