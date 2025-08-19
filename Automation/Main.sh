#!/bin/bash

#Cleanup

nohup rm -r DataStorage/RunData/Primary &
wait



#Run a script for 20M steps with no output, to equilibrate. Then, run it for a further 15x2 million steps to generate transitions

cd RunScripts
rm EquilParams.dat
echo "variable randomseed equal $(od -An -N2 -i /dev/urandom)" > EquilParams.dat
cd ../AncillaryScripts

##!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!##
nohup ./lmp_mpi -in ../RunScripts/EquilKinked.lam &


wait


cd RunScripts
for i in $(seq 1 15);
do
    r1=$(od -An -N2 -i /dev/urandom)
    echo "variable randomseed equal ${r1}" > TransParams.dat
    echo "variable foldername index ../DataStorage/RunData/Primary/$i" >> TransParams.dat

    cd ../AncillaryScripts

##!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!##
    nohup ./lmp_mpi -in ../RunScripts/TransKinked.lam &
    
    cd ../RunScripts

    sleep 5

    mv nohup.out ../DataStorage/RunData/Primary/$i/nohup.out

    rm TransParams.dat
done
cd ../AncillaryScripts
wait

#Use pre-prepared scripts to find the transitions and determine which restart files to use
cd ..
for i in $(seq 1 15);
do
	nohup ./AncillaryScripts/RunKymoOnDir2.x DataStorage/RunData/Primary/$i 2000000 1 200 1 Primary/$i &
done
wait

for i in $(seq 1 15);
do
	mv DataStorage/KymoOutputs/Primary/$i/BU__KN_3_1.n200.topo.dat DataStorage/KymoOutputs/Primary/$i/KymoOut_Primary_$i.dat
done

sleep 1

rm DataStorage/RestartNumbers.dat
for i in $(seq 1 15);
do
	cd AncillaryScripts
	nohup python FindRestartFiles.py Primary/$i Primary/$i 1000 &
	wait
	cd ..
done


#Restart simulations in batches of 25 for a short time, then use a prepared script to find transitions in the 25, move the results to the consolidated folder, and start the next 25.

cd DataStorage/KymoOutputs
nohup rm -r Repeats &
wait
mkdir Repeats
cd ../..

cd AncillaryScripts
for i in $(seq 1 20);
do
	for j in $(seq 1 25);
	do
		let "RepNum = 25*$i + $j - 25"
		RandomFile=$(shuf -n 1 ../DataStorage/RestartNumbers.dat)
		cd ../RunScripts
		rm RepParams.dat
		r1=$(od -An -N2 -i /dev/urandom)
    		echo "variable randomseed equal ${r1}" > RepParams.dat
    		echo "variable foldername index ../DataStorage/RunData/Repeats/${RepNum}" >> RepParams.dat
		echo "variable restartDirectory index ../${RandomFile}" >> RepParams.dat

		cd ../AncillaryScripts
		##!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!##
    		nohup ./lmp_mpi -in ../RunScripts/RepKinked.lam &

		sleep 1
	done

	wait

	cd ..
	for j in $(seq 1 25);
	do
		let "RepNum = 25*$i + $j - 25"
        	nohup ./AncillaryScripts/RunKymoOnDir2.x DataStorage/RunData/Repeats/${RepNum} 50000 1 200 1 Repeats/$j &
	done

	wait

	for j in $(seq 1 25);
	do
		let "RepNum = 25*$i + $j - 25"
		cd DataStorage/KymoOutputs/Repeats/
		FILENAME="$(echo "$j" | tr -d /)"
		mv ./$j/KymoOut_Repeats_${FILENAME}.dat ${RepNum}.dat
	
		sleep .2

		nohup rm -r ./$j &

		cd ../../..
	done

	wait

	cd AncillaryScripts
done

#After everything finishes running, run the Kymo consolidating script on all of the results
cd ..

for j in $(seq 1 15);
do
	nohup rm -r DataStorage/RunData/Primary/$j &
done

wait

python AncillaryScripts/ConsolidateKymoOutputs.py DataStorage/KymoOutputs/Repeats

#Move the finished csv to Automation root.
mv DataStorage/KymoOutputs/Repeats/CondensedOutput.csv .
mv DataStorage/KymoOutputs/Repeats/SteadyStateKnottingCounts.csv .
mv DataStorage/KymoOutputs/Repeats/Percents.csv .
