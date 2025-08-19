#!/bin/bash

cd 3_1

for i in $(seq 1 35);
do
	for k in $(seq 1 10);
	do
		for j in $(seq 1 20);
        	do
                	let "SimNum = 200*$i - 200 + 20*$k - 20 + $j + 10000"
                	let "ResetTime = 100*$i"
                	nohup python ../OneDimensionalLangevin_ResetTime2.py ${ResetTime} ${SimNum} &
        	done
        	wait
	done
done	

rm nohup.out
