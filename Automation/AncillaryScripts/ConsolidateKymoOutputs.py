import argparse
import numpy as np
import os
import pandas as pd
import re

#Parse Input
parser = argparse.ArgumentParser()
parser.add_argument("Identifier")
args = parser.parse_args()

#This marks the file we are looking for
Identifier = args.Identifier

os.chdir(Identifier)

master_top_list = []
master_swap_list = []
master_file_list = []
topology_data = []
#Open each file in directory, and add its contents to the master file
for filename in os.listdir(os.getcwd()):
   with open(os.path.join(os.getcwd(), filename), 'r') as f: # open in readonly mode
       #Remove header
        f.readline()
        f.readline()
        f.readline()
        
        #Loop over all remaining lines and extract topology. removing duplicates
        x='a'
        j = 0
        i = -1
        top_list = []

        while(x!= ''):
            
            i = i + 1
            
            x = f.readline()
            position = x.rfind("_")
            
            if(x != ''):
                if position != -1:
                    topology = x[position-2:position+3:1].replace('\t', ' ')
                else:
                    topology = " UN "
                
                top_list.append(topology)
                
                if i!=0:
                    if top_list[i] == top_list[i-1]:
                        top_list.pop(i)
                        i = i-1
                    else:
                        master_swap_list.append(j) 
                        #Defined to be the index of the time step in which the swap has been completed
                        #i.e. if frame 0 is the first frame, and between the second and third frames
                        #you observed UN -> 3_1, then the index will record as 2.
                        
                        master_file_list.append(filename)
                        
                        master_top_list.append(top_list[i-1] + '->' + top_list[i])

                j = j + 1
                topology_data.append([j, topology])
                    
        #Close file
        f.close()

        
#Fetch the force data for each transition and catalogue that too
force_components = [[],[],[]]
proj_forces = [[],[],[]]
force_components2 = [[],[],[]]
proj_forces2 = [[],[],[]]
fail_indices = []
for j in range(len(master_swap_list)):
    try:
        f = open("../../RunData/Repeats/"+ re.search(r'\d+', master_file_list[j]).group() + "/knot3_1.n200.forces." + str(master_swap_list[j] - 1), 'r')
    except:
        fail_indices.append(j)
        continue

    #Clear out the header
    x = f.readline()
    x = f.readline()
    x = f.readline()
    x = f.readline()
    x = f.readline()
    x = f.readline()
    x = f.readline()
    x = f.readline()
    x = f.readline()
    x = f.readline()
    
    while(x!=''):
        
        y = re.search("^([\S]+)", x).group()
            
        if int(y) == 3:
            tabs = [m.start() for m in re.finditer(' ', x)]
            force_components[0].append(float(x[tabs[0]+1:tabs[1]]))
            force_components[1].append(float(x[tabs[1]+1:tabs[2]]))
            force_components[2].append(float(x[tabs[2]+1:-1]))
            
        x = f.readline()
        
    f.close()
    
    try:
        f1 = open("../../RunData/Repeats/"+ re.search(r'\d+', master_file_list[j]).group() + "/knot3_1.n200." + str(master_swap_list[j] - 1), 'r')
        f2 = open("../../RunData/Repeats/"+ re.search(r'\d+', master_file_list[j]).group() + "/knot3_1.n200." + str(master_swap_list[j]), 'r')
    except:
        fail_indices.append(j)
        continue

    x1 = f1.readline()
    x1 = f1.readline()
    x1 = f1.readline()
    x1 = f1.readline()
    x1 = f1.readline()
    x1 = f1.readline()
    x1 = f1.readline()
    x1 = f1.readline()
    x1 = f1.readline()
    x1 = f1.readline()
    
    x2 = f2.readline()
    x2 = f2.readline()
    x2 = f2.readline()
    x2 = f2.readline()
    x2 = f2.readline()
    x2 = f2.readline()
    x2 = f2.readline()
    x2 = f2.readline()
    x2 = f2.readline()
    x2 = f2.readline()
    
    distances1 = list(range(200))
    distances1[2] = 100000000
    positions1 = list(range(200))
    while(x1 !=''):
        
        y = re.search("^([\S]+)", x1).group()
        y = int(y)
        
        tab_list = []
        tabs = [m.start() for m in re.finditer(' ', x1)]

        nx = float(x1[tabs[3]+1:tabs[4]])
        ny = float(x1[tabs[4]+1:tabs[5]])
        nz = float(x1[tabs[5]+1:tabs[6]])
        
        tab_list.append(float(x1[tabs[0]+1:tabs[1]]) + 100*nx)
        tab_list.append(float(x1[tabs[1]+1:tabs[2]]) + 100*ny)
        tab_list.append(float(x1[tabs[2]+1:tabs[3]]) + 100*nz)
        
        positions1[y-1] = tab_list
        
        x1 = f1.readline()
        
    f1.close()
    
    for n in range(len(positions1)):
        if n!= 2:
            distance = np.sqrt(np.dot(np.array(positions1[n]) - np.array(positions1[2]), np.array(positions1[n]) - np.array(positions1[2])))
            distances1[n] = distance
            
    distances2 = list(range(200))
    distances2[2] = 100000000
    positions2 = list(range(200))
    while(x2 !=''):
        
        y = re.search("^([\S]+)", x2).group()
        y = int(y)
        
        tab_list = []
        tabs = [m.start() for m in re.finditer(' ', x2)]
        
        nx = float(x2[tabs[3]+1:tabs[4]])
        ny = float(x2[tabs[4]+1:tabs[5]])
        nz = float(x2[tabs[5]+1:tabs[6]])
        
        tab_list.append(float(x2[tabs[0]+1:tabs[1]]) + 100*nx)
        tab_list.append(float(x2[tabs[1]+1:tabs[2]]) + 100*ny)
        tab_list.append(float(x2[tabs[2]+1:tabs[3]]) + 100*nz)
        
        positions2[y-1] = tab_list

        x2 = f2.readline()
        
    f2.close()
    
    for n in range(len(positions2)):
        if n!= 2:
            distance = np.sqrt(np.dot(np.array(positions2[n]) - np.array(positions2[2]), np.array(positions2[n]) - np.array(positions2[2])))
            distances2[n] = distance
            
    av_distances = np.divide(np.array(distances1) + np.array(distances2), 2)
    for m in range(5):
        av_distances[m] = 100000000000
    
    closest_bead = np.argmin(av_distances) + 1
        
    normal_vector = np.array(positions2[closest_bead - 1]) - np.array(positions2[2])
    normal_vector = normal_vector / np.linalg.norm(normal_vector)
    
    proj_force_mag = np.dot(normal_vector, np.array([force_components[0][-1], force_components[1][-1], force_components[2][-1]]))
    
    proj_force = normal_vector * proj_force_mag
    
    proj_forces[0].append(proj_force[0])
    proj_forces[1].append(proj_force[1])
    proj_forces[2].append(proj_force[2])
    
    try:
        f = open("../../RunData/Repeats/"+ re.search(r'\d+', master_file_list[j]).group() + "/knot3_1.n200.forces." + str(master_swap_list[j] - 1), 'r')
    except:
        continue

    x = f.readline()
    x = f.readline()
    x = f.readline()
    x = f.readline()
    x = f.readline()
    x = f.readline()
    x = f.readline()
    x = f.readline()
    x = f.readline()
    x = f.readline()

    while(x!=''):
        y = re.search("^([\S]+)", x).group()

        if int(y) == closest_bead:
            tabs = [m.start() for m in re.finditer(' ', x)]
            force_components2[0].append(float(x[tabs[0]+1:tabs[1]]))
            force_components2[1].append(float(x[tabs[1]+1:tabs[2]]))
            force_components2[2].append(float(x[tabs[2]+1:-1]))

        x = f.readline()

    f.close()

    proj_force_mag2 = np.dot(normal_vector, np.array([force_components2[0][-1], force_components2[1][-1], force_components2[2][-1]]))

    proj_force2 = normal_vector * proj_force_mag2

    proj_forces2[0].append(proj_force2[0])
    proj_forces2[1].append(proj_force2[1])
    proj_forces2[2].append(proj_force2[2])

fail_indices.sort(reverse=True)
if fail_indices != []:
    for j in fail_indices:
        master_file_list.pop(j)
        master_top_list.pop(j)
        master_swap_list.pop(j)

dictionary = {"Filename": master_file_list,
              "Topologies": master_top_list,
              "Swap Indices": master_swap_list,
              "Seg Force x": force_components[0],
              "Seg Force y": force_components[1],
              "Seg Force z": force_components[2],
              "Seg Proj Force x": proj_forces[0],
              "Seg Proj Force y": proj_forces[1],
              "Seg Proj Force z": proj_forces[2],
              "Pass Force x": force_components2[0],
              "Pass Force y": force_components2[1],
              "Pass Force z": force_components2[2],
              "Pass Proj Force x": proj_forces2[0],
              "Pass Proj Force y": proj_forces2[1],
              "Pass Proj Force z": proj_forces2[2]}

for key in dictionary.keys():
    print(key, len(dictionary[key]))

dataframe = pd.DataFrame(data=dictionary, columns=["Filename", "Topologies", "Swap Indices", "Seg Force x", "Seg Force y", "Seg Force z", "Seg Proj Force x", "Seg Proj Force y", "Seg Proj Force z", "Pass Force x", "Pass Force y", "Pass Force z", "Pass Proj Force x", "Pass Proj Force y", "Pass Proj Force z"])

dataframe.to_csv("./CondensedOutput.csv")

master_top_list = []
#Open each file in directory, and add its contents to the master file
for filename in os.listdir(os.getcwd()):
   with open(os.path.join(os.getcwd(), filename), 'r') as f: # open in readonly mode
       #Remove header
        f.readline()
        f.readline()
        f.readline()

        #Loop over all remaining lines and extract topology.
        x='a'
        topology_list = []

        while(x!= ''):

            x = f.readline()
            position = x.rfind("_")

            if(x != ''):
                if position != -1:
                    topology = x[position-2:position+3:1].replace('\t', ' ')
                else:
                    topology = " UN "

                master_top_list.append(topology)

        #Close file
        f.close()

found_list = []
data_list = []
index_dict = {}
j = 0
for i in range(len(master_top_list)):
    if master_top_list[i] not in found_list:
        found_list.append(master_top_list[i])
        data_list.append(0)
        index_dict.update({master_top_list[i]: j})
        j = j+1

    data_list[index_dict[master_top_list[i]]] = data_list[index_dict[master_top_list[i]]] + 1

dictionary = {"Topologies": found_list,
              "Counts": data_list}

dataframe = pd.DataFrame(data=dictionary, columns=["Topologies", "Counts"])

dataframe.to_csv("./SteadyStateKnottingCounts.csv")

percents = list(range(50000))
totals = list(range(50000))
counts = list(range(50000))
for i in range(len(percents)):
    percents[i] = 0
    totals[i] = 0
    counts[i] = 0

for data in topology_data:
    step = data[0]
    top = data[1]

    if top == " UN ":
        totals[step - 1] = totals[step - 1] + 1
    counts[step - 1] = counts[step - 1] + 1

for i in range(len(percents)):
    percents[i] = totals[i] / counts[i]

dictionary = {"Percents": percents}
dataframe = pd.DataFrame(data=dictionary, columns=["Percents"])
dataframe.to_csv("./Percents.csv")
