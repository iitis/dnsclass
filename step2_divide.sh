#!/bin/bash
# Author: Paweł Foremski <pjf@iitis.pl>
# Copyright (C) 2012-2013 IITiS PAN Gliwice
# Licensed under GNU GPL v3 (see the LICENSE file)

FACTOR=0.6

if [[ $# -lt 1 ]]; then
	echo "usage: $0 outdir" >&2
	exit 1
fi

OUTDIR="$1"
shift

echo "Random sort..."
shuf $OUTDIR/data.txt > $OUTDIR/shuffled.txt

set -- `wc -l $OUTDIR/shuffled.txt`
SIZE="$1"

TRAIN=`echo "$FACTOR * $SIZE" | bc`
TEST=`echo "$SIZE - $TRAIN" | bc`
TEST1=`echo "$TEST / 2" | bc`
TEST2=`echo "$TEST - $TEST1" | bc`

tr="${TRAIN%.*}"
cv="${CV%.*}"
te="${TEST%.*}"
te1="${TEST1%.*}"
te2="${TEST2%.*}"
fil="${FILE%.*}"

echo "Putting $tr in $OUTDIR/train.txt ..."
head -n $tr $OUTDIR/shuffled.txt > $OUTDIR/train.txt

#tail -n $te $OUTDIR/shuffled.txt > $OUTDIR/tmp.txt
#	echo "Putting $te1 in $OUTDIR/cv.txt ..."
#	head -n $te1 $OUTDIR/tmp.txt > $OUTDIR/cv.txt
#
#	echo "Putting $te2 in $OUTDIR/test.txt ..."
#	tail -n $te2 $OUTDIR/tmp.txt > $OUTDIR/test.txt
#rm -f $OUTDIR/tmp.txt
tail -n $te $OUTDIR/shuffled.txt > $OUTDIR/test.txt
