#!/bin/bash

#Format: {path from Automation to Dir}, {Number of steps}, {time step}, {number of beads}, {number of polymers}, {identifier}

mf=`pwd`

cd AncillaryScripts
  
cd ./../KymoKnot-master/
make
make

cd ../DataStorage/KymoOutputs

rm -r $6
mkdir $6

cd ../../AncillaryScripts

c++  MakeKnotFile.c++ -o  MakeKnotFile

wait

cp MakeKnotFile ../DataStorage/KymoOutputs/$6
cd ../DataStorage/KymoOutputs/$6

./MakeKnotFile ../../../$1/knot3_1.n200. 3_1.n200.topo.dat $2 $3 $4 $5

wait

../../../KymoKnot-master/KymoKnot_ring.x -s 20 KN_3_1.n200.topo.dat

wait

mv BU__KN_3_1.n200.topo.dat KymoOut_$6.dat
