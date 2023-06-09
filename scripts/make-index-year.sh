#!/bin/bash

CUR_YEAR=$(date +%Y)
FIRST_YEAR=2004
#FIRST_YEAR=1999

mkdir -p data/archive
for i in $(seq $CUR_YEAR -1 $FIRST_YEAR) ; do
  if [ $i == $CUR_YEAR ] ; then
		rm -fv data/archive/$i.md
		continue
	fi
	cat templates/archive-year.md | sed "s/XXXX/$i/g" > data/archive/$i.md

	echo "---" >> data/archive/$i.md
	echo -ne "*Archives: " >> data/archive/$i.md
	for j in $(seq $CUR_YEAR -1 $FIRST_YEAR) ; do
		if [ $j = $i ] ; then
			echo -n "$j" >> data/archive/$i.md
		elif [ $j = $CUR_YEAR ] ; then
			echo -ne "[$j](/)" >> data/archive/$i.md
		else
			echo -ne "[$j](/archive/$j)" >> data/archive/$i.md
		fi
		if [ $j != $FIRST_YEAR ] ; then
			echo -ne " | " >> data/archive/$i.md
		fi
	done
	echo "*" >> data/archive/$i.md
done

