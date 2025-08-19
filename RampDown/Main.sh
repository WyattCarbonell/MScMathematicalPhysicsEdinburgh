#!/bin/bash
cd RunScripts/
for i in $(seq 1 10)
do
	for j in $(seq 1 10)
	do
		let "scriptnumber = 10*$i + $j - 10"
		cd ../RunScripts
		rm EquilParams.dat
		echo "variable randomseed equal $(od -An -N2 -i /dev/urandom)" > EquilParams.dat
		echo "variable scriptnumber equal ${scriptnumber}" >> EquilParams.dat
		cd ../AncillaryScripts
		sleep 2.5
		#echo "$(<../RunScripts/EquilParams.dat)"
		nohup ./lmp_mpi -in ../RunScripts/EquilUnkinked.lam &
	done

	cd ..

	wait

	for j in $(seq 1 10);
	do
		let "scriptnumber = 10*$i + $j - 10"
        	nohup ./AncillaryScripts/RunKymoOnDir.x DataStorage/RunData/Primary/${scriptnumber} 10000 1 200 1000 ${scriptnumber} &
	done

	wait

	for j in $(seq 1 10);
	do		
		let "scriptnumber = 10*$i + $j - 10"
        	mv DataStorage/KymoOutputs/${scriptnumber}/KymoOut_${scriptnumber}.dat DataStorage/KymoOutputs/KymoOut_${scriptnumber}.dat
		rm -r DataStorage/KymoOutputs/${scriptnumber}
	done
	cd RunScripts/
done

