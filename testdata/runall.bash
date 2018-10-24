#!/usr/bin/env bash

for f in $(ls *.py)
do
	own=$0
	[[ $f != ${own##*/} ]] &&  ../run.py -n $f -m 1 -d
done
