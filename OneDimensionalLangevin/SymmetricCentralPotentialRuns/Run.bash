#!/bin/bash

cd 3_1

for i in $(seq 1 10);
do
	for l in $(seq 1 5);
	do
		for m in $(seq 1 5);
		do
			for k in $(seq 1 2);
			do
				for j in $(seq 1 20);
        			do
                			let "SimNum = 1000*$i - 1000 + 100*$k - 100 + $j + 100000*$l + 1000000*$m + 1000000000"
                			let "ResetTime = 200*$i - 100"
                			nohup python ../OneDimensionalLangevin_Area2.py ${ResetTime} $l $m ${SimNum} &
        			done
        			wait
			done
		done
	done
done	

rm nohup.out
