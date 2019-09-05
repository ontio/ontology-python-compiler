#!/usr/bin/env bash
set -ev
oldir=$(pwd)
currentdir=$(dirname $0)
cd $currentdir

../ontology_test/example/runall-testing.bash

testdir="../ontology_test/example/OffChainOp"
$testdir/runall-testing.bash

for avm in $(ls ${testdir}/*.avm.str)
do
	./ontowasm -b $avm
done
cd $oldir
