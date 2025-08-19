import argparse
import numpy as np

#Parse Input
parser = argparse.ArgumentParser()
parser.add_argument("Identifier")
parser.add_argument("RestartDataDir")
parser.add_argument("RestartFrequency")
args = parser.parse_args()

#This marks the file we are looking for
Identifier = args.Identifier

#This marks the location of the restart files
RDD = args.RestartDataDir

#This marks how often restart files are generated
RF = int(args.RestartFrequency)

#Read file
ID2 = Identifier.replace('/', '_')
f = open("../DataStorage/KymoOutputs/" + Identifier + "/KymoOut_" + ID2 + ".dat", 'r')

#Remove header
f.readline()
f.readline()
f.readline()

#Loop over all remaining lines and extract topology, removing duplicates.
x='a'
i = -1
j = 0
topology_list = []
swap_indices_list = []

while(x!= ''):
    
    i = i + 1
    
    x = f.readline()
    position = x.rfind("_")
    
    if(x != ''):
        if position != -1:
            topology = x[position-2:position+3:1].replace('\t', ' ')
        else:
            topology = " UN "
        
        topology_list.append(topology)
        
        if i!=0:
            if topology_list[i] == topology_list[i-1]:
                topology_list.pop(i)
                i = i-1
            else:
                swap_indices_list.append(j) 
                #Defined to be the index of the time step in which the swap has been completed
                #i.e. if frame 0 is the first frame, and between the second and third frames
                #you observed UN -> 3_1, then the index will record as 2.
                
        j = j + 1
            
#Close file
f.close()

swap_indices_array = np.array(swap_indices_list)

if swap_indices_array.size != 0:
    restart_file_numbers_array = np.round(np.divide(swap_indices_array, np.repeat(RF, swap_indices_array.size)))*RF
else:
    restart_file_numbers_array = np.array([])

f = open("../DataStorage/RestartNumbers.dat", 'a')
temp = ''
for number in restart_file_numbers_array:
    number = int(number)
    if number != temp:
        f.write("DataStorage/RunData/" + RDD + "/Restarts/Restart.knot3_1.n200." + str(number) + "\n")
    temp = number

f.close()
