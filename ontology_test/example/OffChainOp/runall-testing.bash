#!/usr/bin/env bash

total=0
correct=0
prefix="../"

function success {
  printf "\e[32m$1\e[m\n"
}

function error {
  printf "\e[31m$ERROR $1\e[m\n"
}

function compiler {
	ls *.py > /dev/null 2>&1

	[[ $? -eq 0 ]] && {
		for f in $(ls *.py)
		do
			own=$0
			[[ $f != ${own##*/} ]] && ${prefix}/../../run.py -n $f -m 1
			returnstatus=$?
		
			((total++))
			if [[ $returnstatus == 0 ]]
			then
				((correct++))
				success "$f"
			else
				error "$f"
			fi
		done
	}
}

olddir=$(pwd)
currentdir=$(dirname $0)
cd $currentdir
compiler
cd $oldir

[[ $correct == $total ]] && { echo "${correct}/${total} Files Compiled Successfully";exit 0; } || { echo "${correct}/${total} Files Compiled Failed."; exit 1; }
