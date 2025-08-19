#!/bin/bash
cd data

for i in $(seq 1 2);
do
	for l in $(seq 1 5);
	do
		for m in $(seq 1 5);
		do
			for k in $(seq 1 10);
			do
				for j in $(seq 1 10);
        			do
                			let "SimNum = 200*$i - 200 + 20*$k - 20 + $j + 10000*$l + 100000*$m"
                			let "ResetTime = 100*$i"
                			nohup python ../OneDimensionalLangevin_Area.py ${ResetTime} $l $m ${SimNum} &
        			done
        			wait
			done
		done
	done
done	
