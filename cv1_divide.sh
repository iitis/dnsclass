#!/bin/bash
# Author: Paweł Foremski <pjf@iitis.pl>
# Copyright (C) 2012-2013 IITiS PAN Gliwice
# Licensed under GNU GPL v3 (see the LICENSE file)

if [ $# -lt 2 ]; then
	echo "usage: cv1_divide.sh dir/ k" >&2;
	exit 1
fi

DIR="$1"
K="$2"

function doit()
{
	I="$1"
	FROM="$2"
	TO="$3"

	echo "putting lines $FROM till $TO to $DIR/cv${I}.txt..."
	sed $DIR/shuffled.txt -ne "${FROM},${TO}p" > $DIR/cv${I}.txt
}

echo "shuffling..."
shuf $DIR/data.txt > $DIR/shuffled.txt

echo -n "counting... "
set -- `wc -l $DIR/shuffled.txt`
NUM="$1"
PERFILE=$((NUM / K))
echo "$NUM lines -> $PERFILE per file"

for i in `seq 0 $((K-2))`; do
	doit "$((i+1))" "$((PERFILE*i+1))" "$((PERFILE*(i+1)))" &
done
doit "$K" "$((PERFILE*(K-1)+1))" "$NUM" &
