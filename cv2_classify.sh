#!/bin/bash
# Author: Paweł Foremski <pjf@iitis.pl>
# Copyright (C) 2012-2013 IITiS PAN Gliwice
# Licensed under GNU GPL v3 (see the LICENSE file)

if [ $# -lt 4 ]; then
	echo "usage: cv1_divide.sh dir/ k from to [OPTIONS...]" >&2;
	exit 1
fi

DIR="$1"
K="$2"
FROM="$3"
TO="$4"

shift 4
OPTS="$@"

function doit()
{
	I="$1"

	rm -fr $DIR/cv$I
	mkdir -p $DIR/cv$I

	# connect files
	for j in `seq 1 $K`; do
		if [ "$j" = "$I" ]; then
			echo "$I: use $j for testing"
			cat $DIR/cv$j.txt > $DIR/cv$I/test.txt
		else
			echo "$I: add $j"
			cat $DIR/cv$j.txt >> $DIR/cv$I/train.txt
		fi
	done

	# convert and train
	./step3_convert_train.py $OPTS $DIR/cv$I || exit 1
	./step4_train.sh $DIR/cv$I -f || exit 2

	# convert and test
	./step5_convert_test.py $OPTS $DIR/cv$I $DIR/cv$I/test.txt || exit 3
	./step6_predict.py $OPTS -s $DIR/cv$I $DIR/cv$I/test.txt || exit 4

	# analyze
	./step7_analyze.py $OPTS $DIR/cv$I $DIR/cv$I/test.txt || exit 5
}

for FOLD in `seq $FROM $TO`; do
	echo "================== fold $FOLD ================="
	doit $FOLD &
done
