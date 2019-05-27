#!/usr/bin/env bash

total=0
correct=0

function success {
  printf "\e[32m$1\e[m\n"
}

function error {
  printf "\e[31m$ERROR $1\e[m\n"
}

for f in $(ls *.py)
do
	own=$0
	x=$([[ $f != ${own##*/} ]] && ../../run.py -n $f -m 1 -t)
	total=$[$total+1]
	if [ $x == 1 ]
	then
		correct=$[$correct+1]
		success "$f"
	else
		error "$f"
	fi
done
echo "$correct/$total Files Compiled Successfully"
if [ $correct == $total ]
then
	return 1
else
	return 0
fi
