#!/usr/bin/env bash
set -ev

oldir=$(pwd)
currentdir=$(dirname $0)
cd $currentdir

for f in $(ls *.py)
do
	../../../run.py -n $f -m 1
done
#rm *.avm.str
#rm *.warning
#rm *.debug.json
#rm *.abi.json
#rm *.Func.Map

rm -f ../testwasmdata/*
mkdir -p ../testwasmdata/
mv  *.avm ../testwasmdata/

cd $oldir
cd ../
./wasm-test
