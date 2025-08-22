import numpy as np
import os
import pandas as pd
import re

num_list = []
#Find files with data
os.chdir("DataStorage/KymoOutputs/Repeats/")
for file in os.listdir(os.getcwd()):
    num = file[0:file.find(".")]
    num_list.append(num)

os.chdir("../../RunData/Repeats/")

start_tops = []
end_tops = []
transitions = []
net_force_list = []

for RepNum in num_list:
    try:
        os.chdir(str(RepNum))
    except:
        continue
    
    print(RepNum)
    #Find all steps in which Topo-II is active
    ActiveSteps = []
    
    for StepNum in range(50001):
        with open(os.path.join(os.getcwd(), "knot3_1.n200." + str(StepNum)), 'r') as f_pos: # open in readonly mode
            
            #clear the header
            f_pos.readline()
            f_pos.readline()
            f_pos.readline()
            f_pos.readline()
            f_pos.readline()
            f_pos.readline()
            f_pos.readline()
            f_pos.readline()
            f_pos.readline()
            
            #Get the first line of data
            x = f_pos.readline()
            
            while(x!=''):
                
                #find separations between entries
                tabs = [m.start() for m in re.finditer(' ', x)]
                
                #the AtomType is the second number
                AtomType = x[tabs[0]+1:tabs[1]]
                
                #If an atom is in an active state, put it in the active state list
                if AtomType == "4":
                    ActiveSteps.append(StepNum)
                    break
                
                #Continue to the next line
                x = f_pos.readline()
                
            #close the file
            f_pos.close()



    #Now that we know when Topo-II is active, we can determine whether it was activated multiple times, and when the activations led to a transition
    
    #Determine the independent periods in which Topo-II is active
    ActivationRanges = []
    
    for i in range(len(ActiveSteps)-1):
        End_step = 0
        
        if i == 0:
            try:
                ActiveSteps[i]
                Start_step = ActiveSteps[0]
            except:
                break
            
        else:
            if ActiveSteps[i] == ActiveSteps[i+1] - 1:
                if i == len(ActiveSteps)-2:
                    End_step = ActiveSteps[i+1]
                    ActivationRanges.append((Start_step, End_step))
                    continue
                else:    
                    continue
            else:
                End_step = ActiveSteps[i]
                ActivationRanges.append((Start_step, End_step))
                Start_step = ActiveSteps[i+1]
    
    #Now we find the net force on the Topo-II through the full activation period
    
    net_forces = []
    
    for i in range(len(ActivationRanges)):
        start, end = ActivationRanges[i]
        
        net_force = [0, 0, 0]
        
        for step in range(start, end+1):
            with open(os.path.join(os.getcwd(), "knot3_1.n200.forces." + str(step)), 'r') as f_forces: # open in readonly mode
                #Clear the header
                f_forces.readline()
                f_forces.readline()
                f_forces.readline()
                f_forces.readline()
                f_forces.readline()
                f_forces.readline()
                f_forces.readline()
                f_forces.readline()
                f_forces.readline()
                
                #Get the first data line
                x = f_forces.readline()
                
                while(x!=''):
        
                    #Find the bead number
                    y = re.search("^([\S]+)", x).group()
                        
                    #If the bead is part of Topo-II, grab the force components
                    if int(y) in [1, 2, 3, 4, 5]:
                        tabs = [m.start() for m in re.finditer(' ', x)]
                        net_force[0] += float(x[tabs[0]+1:tabs[1]])
                        net_force[1] += float(x[tabs[1]+1:tabs[2]])
                        net_force[2] += float(x[tabs[2]+1:-1])
                        
                    x = f_forces.readline()
        
                f_forces.close()
                
        net_forces.append(np.sum(np.power(net_force, 2)))
        
    #Now, we need to extract the topology information to determine whether a transition occurred.
    os.chdir("../../../KymoOutputs/Repeats/")
        
    top_list = []
    with open(os.path.join(os.getcwd(), str(RepNum) + ".dat"), 'r') as f: # open in readonly mode
        #Remove header
        f.readline()
        f.readline()
        f.readline()
            
        #Loop over all remaining lines and extract topology.
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
                        
        #Close file
        f.close()
        
    #Assemble a complete data point and add it to the data list
    for i in range(len(ActivationRanges)):
        start, end = ActivationRanges[i]
        try:
            start_top = top_list[start]
            end_top = top_list[end]
        except:
            continue
        
        #Determine whether a passage occurred. Note that we have to check for both a topological change or a passage and escape. It is possible, though unlikely, that a passage is missed if topology is preserved and the strand always stays close to the Topo-II
        if ((end - start < 5000) and (end != 50000) and (start!=0)) or (start_top != end_top):
            transition = True
        else:
            transition = False
            
        net_force = net_forces[i]
        
        start_tops.append(start_top)
        end_tops.append(end_top)
        transitions.append(transition)
        net_force_list.append(net_force)
        
    #Reset to the original directory
    os.chdir("../../RunData/Repeats/")
    
#Now that all of the data is collected, export it.
dictionary = {"Start": start_tops,
              "End": end_tops,
              "Transition": transitions,
              "NetForce": net_force_list}

dataframe = pd.DataFrame(data=dictionary, columns=["Start", "End", "Transition", "NetForce"])

dataframe.to_csv("./CollisionData.csv")

        
        
        
