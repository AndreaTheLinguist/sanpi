#! /bin/tcsh -f

lsc-train 20 50 vo.txt |\
lsc-print -n 10 >! model-20
